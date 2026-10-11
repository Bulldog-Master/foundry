"""Root-custodied one-shot transport; no autonomous activation."""
import datetime, fcntl, json, math, os, pathlib, re, socket, sys, urllib.error, urllib.request, uuid
from runtime_contract import ALLOWED, Reject, adverse, canon, parse, put, read_root, schema, sha, validate_packet, validate_result, verify_release

ETC = pathlib.Path('/etc/foundry-evaluator')
RELEASE = pathlib.Path(__file__).resolve().parent.parent
if not (RELEASE/'profile.json').exists(): RELEASE = pathlib.Path(__file__).resolve().parent
RUNS = pathlib.Path('/var/lib/foundry-evaluator/runs')
API_URL = 'https://api.anthropic.com/v1/messages'

def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def scan(chunks):
    rules = {
        'PRIVATE_KEY':r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----',
        'ANTHROPIC_KEY':r'sk-ant-[A-Za-z0-9_-]{16,}',
        'GITHUB_TOKEN':r'(?:gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})',
        'AWS_KEY':r'AKIA[0-9A-Z]{16}',
        'PERSONAL_EMAIL':r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
        'PERSONAL_SSN':r'\b\d{3}-\d{2}-\d{4}\b',
    }
    hits = set()
    for data in chunks:
        text = data.decode('utf-8')
        for name,pattern in rules.items():
            if re.search(pattern,text): hits.add(name)
        for token in re.findall(r'[A-Za-z0-9_+/=-]{32,}',text):
            if re.fullmatch(r'[0-9a-fA-F]+',token): continue
            if not (re.search('[a-z]',token) and re.search('[A-Z]',token) and re.search('[0-9]',token)): continue
            entropy = -sum((token.count(c)/len(token))*math.log2(token.count(c)/len(token)) for c in set(token))
            if entropy >= 4.8: hits.add('HIGH_ENTROPY_TOKEN')
    return sorted(hits)

def main(argv):
    os.umask(0o077)
    if os.geteuid()!=0: raise Reject('must run as root')
    if len(argv)!=2: raise Reject('usage: foundry-evaluator-invoke PACKET_DIR')
    verify_release(RELEASE)
    profile = parse(read_root(RELEASE/'profile.json'))
    task = read_root(RELEASE/'evaluator-task.md')
    m,members = validate_packet(argv[1],profile,task)
    cfg = parse(read_root(RELEASE/'config.json'))
    if cfg != {'model':'claude-opus-5-5','max_tokens':32000,'effort':'high'}: raise Reject('configuration drift')
    terms = read_root(RELEASE/'provider-terms.json')
    if parse(terms).get('accepted_for')!='public-repository Foundry BOOTSTRAP-0 evaluations only': raise Reject('provider terms not accepted')
    req=urllib.request.Request('https://api.github.com/repos/Bulldog-Master/foundry',headers={'User-Agent':'foundry-evaluator/0.1'})
    with urllib.request.urlopen(req,timeout=60) as response: repo=parse(response.read())
    if repo.get('id')!=m['repository']['repo_id'] or repo.get('private') is not False: raise Reject('private or unknown visibility requires founder disclosure act')
    transmitted=[canon(m),*members.values(),task]
    matches=scan(transmitted)
    run_dir=RUNS/m['packet_sha256']; run_dir.mkdir(parents=True,mode=0o700,exist_ok=True)
    with open(run_dir/'lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if matches:
            target=run_dir/('disclosure-block-'+str(uuid.uuid4())); target.mkdir(mode=0o700)
            put(target,'blocked.json',canon({'packet_sha256':m['packet_sha256'],'matched_rule_ids':matches,'status':'BLOCKED'}))
            raise Reject('pre-transmission disclosure scan blocked: '+','.join(matches))
        disclosure={'scanner_sha256':sha(read_root(pathlib.Path(__file__).resolve())), 'packet_sha256':m['packet_sha256'],
            'repository_visibility':'PUBLIC','fork_visibility':'NOT_A_FORK','members_scanned':len(transmitted),
            'bytes_scanned':sum(map(len,transmitted)),'scan_outcome':'CLEAN','matched_rule_ids':[],
            'provider_terms_sha256':sha(terms),'provider_terms_accepted':True,'founder_decision_sha256':None}
        previous=None
        if (run_dir/'attempt-1').exists():
            try: previous=parse(read_root(run_dir/'attempt-1/invocation-record.json'))
            except (ValueError,OSError): raise Reject('HARD_STOP: interrupted prior attempt')
            if previous['evaluator']['config_sha256']!=sha(canon(cfg)) or previous['evaluator']['system_prompt_sha256']!=sha(task): raise Reject('HARD_STOP: retry configuration drift')
            if previous['schema_validation']=='VALID': raise Reject('valid result already exists; never re-run')
            if previous['transport_outcome']!='COMPLETED' or previous['adverse_signal_scan']['outcome']!='NONE': raise Reject('HARD_STOP: adverse or indeterminate prior output')
            if (run_dir/'attempt-2').exists(): raise Reject('HARD_STOP: attempts exhausted')
        attempt=2 if previous else 1
        adir=run_dir/('attempt-%d'%attempt); adir.mkdir(mode=0o700)
        user=canon({'manifest':m,'members':{k:v.decode('utf-8') for k,v in members.items()}})
        body={'model':cfg['model'],'max_tokens':cfg['max_tokens'],'system':task.decode('utf-8'),
              'messages':[{'role':'user','content':user.decode('utf-8')}],'output_config':{'effort':cfg['effort']}}
        started=now(); raw=bytearray(); outcome='COMPLETED'; request_id='none'; error=None
        key=read_root(ETC/'api-key',100_000).decode().strip()
        request=urllib.request.Request(API_URL,data=canon(body),method='POST',headers={'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'})
        try:
            with urllib.request.urlopen(request,timeout=900) as response:
                request_id=response.headers.get('request-id','none')
                while True:
                    chunk=response.read1(65536)
                    if not chunk: break
                    raw.extend(chunk)
        except urllib.error.HTTPError as e:
            raw.extend(e.read()); outcome='ERROR'; error='HTTP '+str(e.code)
        except Exception as e:
            if getattr(e,'partial',None): raw.extend(e.partial)
            outcome='TIMEOUT' if isinstance(e,(TimeoutError,socket.timeout)) else 'ERROR'
            error=type(e).__name__
        raw=bytes(raw); put(adir,'raw-response.json',raw)
        put(adir,'request-meta.json',canon({'model':cfg['model'],'max_tokens':cfg['max_tokens'],'effort':cfg['effort'],
            'system_prompt_sha256':sha(task),'user_content_sha256':sha(user)}))
        validation='INVALID_MALFORMED'; errors=[]; result=None; model=cfg['model']; routecheck='NOT_APPLICABLE'
        scan_outcome,signals=adverse(raw)
        try:
            if outcome!='COMPLETED': raise Reject('transport '+outcome)
            response=parse(raw); model=response.get('model','unknown')
            if not isinstance(model,str): model='invalid-model-metadata'
            if not (model==cfg['model'] or re.fullmatch(re.escape(cfg['model'])+r'-\d{8}',model)):
                raise Reject('unexpected provider model')
            if response.get('stop_reason')!='end_turn':
                scan_outcome,signals='INDETERMINATE',[]
                raise Reject('truncated or incomplete output')
            if not isinstance(response.get('content'),list) or any(b.get('type')!='text' for b in response['content']): raise Reject('unexpected provider content')
            text=''.join(b['text'] for b in response['content'])
            scan_outcome,signals=adverse(text.encode())
            result=parse(text.encode()); validate_result(result,m,members)
            validation='VALID'; routecheck='MATCHES_TABLE'
        except Exception as e: errors.append(type(e).__name__+': '+str(e)[:1000])
        if outcome!='COMPLETED': scan_outcome,signals='INDETERMINATE',[]
        resultsha=sha(canon(result)) if validation=='VALID' else None
        if resultsha: put(adir,'result.json',canon(result))
        record={'record_schema_version':'0.1','invocation_id':str(uuid.uuid4()),'packet_sha256':m['packet_sha256'],
            'result_sha256':resultsha,'raw_output_sha256':sha(raw) if raw else None,'raw_output_bytes':len(raw),'transport_outcome':outcome,
            'adverse_signal_scan':{'algorithm_version':'0.1','outcome':scan_outcome,'matched_signals':signals},'pre_transmission_disclosure':disclosure,
            'evaluator':{'provider':'anthropic','model_id':model,'config_sha256':sha(canon(cfg)),'system_prompt_sha256':sha(task)},
            'environment':{'session_id_sha256':sha(request_id.encode()),'runtime_image_sha256':sha(read_root(RELEASE/'RUNTIME.json')+read_root(RELEASE/'MANIFEST.sha256')),'host_id_sha256':sha(socket.gethostname().encode())},
            'accessible_context':ALLOWED,'tools_available':[],'network_policy':'none','credentials_present':[],
            'prior_exposure':{'known_prior_sessions_on_this_pr':[],'knowable_limits':'Stateless Messages request, no history or tools. Training exposure is unknowable; no prior findings supplied.'},
            'attempt':attempt,'started_at':started,'completed_at':now(),'schema_validation':validation,'routing_check':routecheck}
        record['review_record_sha256']=sha(canon({'packet_sha256':m['packet_sha256'],'result_sha256':resultsha,'invocation_record_without_hash':record}))
        schema('invocation-record.schema.json',record)
        put(adir,'validation-errors.json',canon(errors+([error] if error else []))); put(adir,'invocation-record.json',canon(record))
        print(json.dumps({'packet_sha256':m['packet_sha256'],'attempt':attempt,'schema_validation':validation,'routing_check':routecheck,
            'run_dir':str(adir),'review_record_sha256':record['review_record_sha256'],'errors':errors},sort_keys=True))
        return 0 if validation=='VALID' else 5 if attempt==1 and outcome=='COMPLETED' and scan_outcome=='NONE' else 4
