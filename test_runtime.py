"""Offline acceptance tests with injected transport and fixture-only custody."""
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import runtime_contract as c
import runtime_invoke as inv

HERE=pathlib.Path(__file__).resolve().parent
REAL_READ=c.read_root

def load(name):
    loader=importlib.machinery.SourceFileLoader(name,str(HERE/name))
    spec=importlib.util.spec_from_loader(name,loader)
    module=importlib.util.module_from_spec(spec); loader.exec_module(module)
    return module

def fixture_read(path,limit=8_000_000):
    path=pathlib.Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o022: raise c.Reject('unsafe fixture')
    data=path.read_bytes()
    if len(data)>limit: raise c.Reject('oversized fixture')
    return data

class Response:
    def __init__(self,raw,fail=False): self.raw=raw; self.fail=fail; self.headers={'request-id':'private-session'}
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self): return self.raw
    def read1(self,n):
        if self.raw:
            data=self.raw; self.raw=b''; return data
        if self.fail: raise TimeoutError('timeout')
        return b''

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.work=pathlib.Path(tempfile.mkdtemp(prefix='foundry-runtime-test-'))
        self.release=self.work/'release'; self.release.mkdir()
        for name in ('config.json','evaluator-task.md','provider-terms.json','MANIFEST.sha256','RUNTIME.json'):
            (self.release/name).write_bytes((HERE/name).read_bytes() if (HERE/name).exists() else b'fixture')
        self.profile=json.loads((HERE/'bootstrap0b-profile.json').read_text())
        (self.release/'profile.json').write_bytes(c.canon(self.profile))
        self.etc=self.work/'etc'; self.etc.mkdir(); (self.etc/'api-key').write_text('fixture-provider-key')
        self.packet=self.work/'packet'; self.packet.mkdir()
        vectors=json.loads((HERE/'CONFORMANCE-VECTORS-v0.1.json').read_text())
        self.m=copy.deepcopy(next(x['instance'] for x in vectors['schema_cases'] if x['schema']=='review-packet.schema.json' and x['expected']=='VALID'))
        self.m['repository']=self.profile['repository']; self.m['head_repository']=self.profile['head_repository']
        self.m['producer_identity']['build_sha256']=c.sha((HERE/'foundry-packet-builder').read_bytes())
        self.m['governance_profile_sha256']=c.sha(c.canon(self.profile)); self.m['evaluator_task']=self.profile['evaluator_task']
        self.m['governance_refs']=[]; self.m['related_context_refs']=[]
        self.members={'diff.patch':b'diff\n','files/a.md':b'one\ntwo\n'}
        self.m['changed_files']=[{'path':'a.md','status':'added','mode':'100644','head_blob_sha':'a'*40,'head_content_sha256':c.sha(self.members['files/a.md']),'size':8,'member':'files/a.md'}]
        self.m['diff']={'member':'diff.patch','sha256':c.sha(self.members['diff.patch']),'git_version':'git version 2.53.0','flags':['--binary','--no-ext-diff','--no-textconv','--full-index']}
        for role,paths,source in [('governing',self.profile['governing_at_base'],'base'),('subject_head_version',self.profile['subject_at_head'],'head')]:
            for i,name in enumerate(paths):
                member=source+'/'+name; data=b'governing text\n'; self.members[member]=data
                self.m['governance_refs'].append({'path':name,'role':role,'source_sha':self.m[source+'_sha'],'sha256':c.sha(data),'member':member})
        self.reseal()
        self.result={'result_schema_version':'0.1','packet_sha256':self.m['packet_sha256'],'pr_number':self.m['pr_number'],'head_sha':self.m['head_sha'],
            'evaluator_task_sha256':self.m['evaluator_task']['sha256'],'routing_profile':c.ROUTING,
            'gates':{g:{'verdict':'PASS','finding_ids':[]} for g in c.PREFIX},'findings':[],'overall':'PASS','routing':'CONTINUE','requires_human':False}
        self.responses=[]; self.requests=[]
        self.patches=[patch.object(c,'read_root',fixture_read),patch.object(inv,'verify_release',lambda p:None),patch.object(inv,'read_root',fixture_read),patch.object(inv,'RELEASE',self.release),patch.object(inv,'ETC',self.etc),patch.object(inv,'RUNS',self.work/'runs'),patch.object(inv.os,'geteuid',lambda:0),patch.object(inv.urllib.request,'urlopen',self.urlopen)]
        for p in self.patches: p.start()
        self.addCleanup(lambda:[p.stop() for p in reversed(self.patches)])
    def reseal(self):
        for name,data in self.members.items():
            path=self.packet/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
        self.m['members']=[{'name':name,'sha256':c.sha(data),'size':len(data)} for name,data in sorted(self.members.items())]
        self.m['completeness']={'complete':True,'truncated':False,'size_bytes':sum(map(len,self.members.values())),'size_limit_bytes':4_000_000}
        self.m.pop('packet_sha256',None); self.m['packet_sha256']=c.sha(c.canon(self.m)); (self.packet/'manifest.json').write_bytes(c.canon(self.m))
    def urlopen(self,request,**kwargs):
        if request.full_url.startswith('https://api.github.com/repos/'):
            return Response(c.canon({'id':1297877588,'private':False}))
        self.requests.append(json.loads(request.data)); return self.responses.pop(0)
    def response(self,text=None,stop='end_turn',fail=False):
        text=c.canon(self.result).decode() if text is None else text
        return Response(c.canon({'model':'claude-opus-5-5','content':[{'type':'text','text':text}],'stop_reason':stop}),fail)
    def invoke(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out): rc=inv.main(['invoke',str(self.packet)])
        return rc,json.loads(out.getvalue())
    def record(self,n=1): return c.parse((self.work/'runs'/self.m['packet_sha256']/('attempt-%d'%n)/'invocation-record.json').read_bytes())
    def test_reasoning_envelopes_extract_only_text_and_preserve_raw(self):
        text=c.canon(self.result).decode(); split=len(text)//2
        blocks=[{'type':'thinking','thinking':'{"verdict":"FAIL"}','signature':'opaque'},
                {'type':'text','text':text[:split]},
                {'type':'redacted_thinking','data':'opaque'},
                {'type':'text','text':text[split:]}]
        raw=c.canon({'model':'claude-opus-5-5','content':blocks,'stop_reason':'end_turn'})
        self.responses=[Response(raw)]; self.assertEqual(self.invoke()[0],0)
        self.assertEqual(self.record()['schema_validation'],'VALID')
        self.assertEqual(self.record()['adverse_signal_scan']['outcome'],'NONE')
        adir=self.work/'runs'/self.m['packet_sha256']/'attempt-1'
        self.assertEqual((adir/'raw-response.json').read_bytes(),raw)
        self.assertEqual((adir/'result.json').read_bytes(),c.canon(self.result))
        self.assertEqual(self.record()['raw_output_sha256'],c.sha(raw))
    def test_reasoning_envelopes_do_not_bypass_verdict_validation(self):
        self.result['head_sha']='d'*40
        blocks=[{'type':'thinking','thinking':c.canon({'verdict':'PASS'}).decode()},
                {'type':'text','text':c.canon(self.result).decode()}]
        self.responses=[Response(c.canon({'model':'claude-opus-5-5','content':blocks,'stop_reason':'end_turn'}))]
        self.assertNotEqual(self.invoke()[0],0)
        self.assertEqual(self.record()['schema_validation'],'INVALID_MALFORMED')
    def test_content_rejects_tools_unknown_and_malformed_blocks(self):
        text={'type':'text','text':c.canon(self.result).decode()}
        for block in ({'type':'tool_use','id':'x','name':'x','input':{}},
                      {'type':'server_tool_use'}, {'type':'future_block'}, {}, None, 'text',
                      {'type':'text'}, {'type':'text','text':None}, {'type':'text','text':7}):
            with self.subTest(block=block), self.assertRaises(c.Reject):
                inv.verdict_text([text,block])
        for content in (None,{},[],[{'type':'thinking'}],[{'type':'redacted_thinking'}],
                        [{'type':'text','text':' '} ]):
            with self.subTest(content=content), self.assertRaises(c.Reject): inv.verdict_text(content)
    def test_tool_use_envelope_never_validates(self):
        blocks=[{'type':'text','text':c.canon(self.result).decode()}, {'type':'tool_use','id':'x','name':'x','input':{}}]
        self.responses=[Response(c.canon({'model':'claude-opus-5-5','content':blocks,'stop_reason':'end_turn'}))]
        self.assertNotEqual(self.invoke()[0],0)
        self.assertEqual(self.record()['schema_validation'],'INVALID_MALFORMED')
    def test_valid_no_tools_minimized_record_and_no_redraw(self):
        self.responses=[self.response()]; rc,out=self.invoke(); self.assertEqual(rc,0)
        record=self.record(); c.schema('invocation-record.schema.json',record)
        self.assertNotIn('tools',self.requests[0]); self.assertEqual(self.requests[0]['max_tokens'],32000)
        self.assertEqual(self.requests[0]['output_config'],{'effort':'high'})
        evidence=(self.work/'runs'/self.m['packet_sha256']/'attempt-1')
        joined=b''.join(p.read_bytes() for p in evidence.iterdir())
        for private in (b'fixture-provider-key',b'private-session'):
            self.assertNotIn(private,joined)
        self.assertEqual(record['environment']['host_id_sha256'],c.sha(inv.socket.gethostname().encode()))
        with self.assertRaisesRegex(c.Reject,'never re-run'): self.invoke()
    def test_malformed_output_hard_stop(self):
        self.responses=[self.response('not json')]; rc,_=self.invoke(); self.assertEqual(rc,4)
        self.assertEqual(self.record()['adverse_signal_scan']['outcome'],'INDETERMINATE')
        with self.assertRaises(c.Reject): self.invoke()
    def test_duplicate_output_hard_stop(self):
        self.responses=[self.response('{"verdict":"PASS","verdict":"FAIL"}')]; rc,_=self.invoke(); self.assertEqual(rc,4)
        self.assertEqual(self.record()['adverse_signal_scan']['outcome'],'INDETERMINATE')
        with self.assertRaises(c.Reject): self.invoke()
    def test_only_complete_nonadverse_invalid_can_retry(self):
        self.responses=[self.response('{}'),self.response()]
        self.assertEqual(self.invoke()[0],5); self.assertEqual(self.invoke()[0],0)
        self.assertTrue((self.work/'runs'/self.m['packet_sha256']/'attempt-1/raw-response.json').exists())
        self.assertEqual(self.record(2)['attempt'],2)
    def test_second_invalid_stops(self):
        self.responses=[self.response('{}'),self.response('{}')]
        self.assertEqual(self.invoke()[0],5); self.assertEqual(self.invoke()[0],4)
        with self.assertRaises(c.Reject): self.invoke()
    def test_partial_timeout_retains_exact_bytes(self):
        self.responses=[Response(b'{"partial":',fail=True)]
        rc,_=self.invoke(); self.assertEqual(rc,4)
        record=self.record(); self.assertEqual(record['transport_outcome'],'TIMEOUT')
        self.assertEqual(record['raw_output_sha256'],c.sha(b'{"partial":'))
        self.assertEqual(record['raw_output_bytes'],11)
        with self.assertRaises(c.Reject): self.invoke()
    def test_truncation_even_complete_text_cannot_retry(self):
        self.responses=[self.response(stop='max_tokens')]
        self.assertEqual(self.invoke()[0],4); self.assertEqual(self.record()['adverse_signal_scan']['outcome'],'INDETERMINATE')
    def test_adverse_invalid_never_redrawn(self):
        self.responses=[self.response('{"verdict":"FAIL"}')]
        self.assertEqual(self.invoke()[0],4); self.assertEqual(self.record()['adverse_signal_scan']['outcome'],'ADVERSE')
        with self.assertRaises(c.Reject): self.invoke()
    def test_security_na_hard_stop_and_valid_failure_not_retried(self):
        self.result['gates']['security']={'verdict':'N/A','finding_ids':[],'na_reason':'specific reason'}
        self.result['routing']='HARD_STOP'; self.result['requires_human']=True
        self.responses=[self.response()]; self.assertEqual(self.invoke()[0],0)
        with self.assertRaises(c.Reject): self.invoke()
    def test_binding_prefix_lines_and_gate_semantics(self):
        r=copy.deepcopy(self.result); r['head_sha']='d'*40
        with self.assertRaises(Exception): c.validate_result(r,self.m,self.members)
        r=copy.deepcopy(self.result); r['gates']['quality']={'verdict':'FAIL','finding_ids':['FND-SEC-001']}; r['overall']='FAIL'; r['routing']='RETURN_TO_OPERATIONS'
        r['findings']=[{'finding_id':'FND-SEC-001','gate':'quality','category':'IMPLEMENTATION_DEFECT','severity':'MAJOR','title':'failure','evidence_refs':[{'member':'files/a.md','line_start':1,'line_end':3}]}]
        with self.assertRaises(Exception): c.validate_result(r,self.m,self.members)
        r['findings'][0]['finding_id']='FND-QUAL-001'; r['gates']['quality']['finding_ids']=['FND-QUAL-001']
        with self.assertRaisesRegex(c.Reject,'line range'): c.validate_result(r,self.m,self.members)
        r['findings'][0]['evidence_refs'][0]['line_end']=2; c.validate_result(r,self.m,self.members)
    def test_packet_tamper_unlisted_symlink_profile(self):
        (self.packet/'extra').write_text('unexpected')
        with self.assertRaises(c.Reject): c.validate_packet(self.packet,self.profile,(self.release/'evaluator-task.md').read_bytes())
        (self.packet/'extra').unlink(); (self.packet/'files/a.md').write_text('tampered')
        with self.assertRaises(c.Reject): c.validate_packet(self.packet,self.profile,(self.release/'evaluator-task.md').read_bytes())
    def test_scan_covers_task_and_manifest_and_credentials(self):
        self.assertIn('PRIVATE_KEY',inv.scan([b'-----BEGIN RSA PRIVATE KEY-----']))
        self.assertIn('PERSONAL_EMAIL',inv.scan([b'person@example.com']))
        self.assertIn('GITHUB_TOKEN',inv.scan([b'ghp_'+b'A'*40]))
        self.assertEqual(inv.scan([b'a'*64]),[])
    def test_canonical_numbers_duplicates_and_adverse_nested(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1.2}',b'{"a":9007199254740992}',b'{"a":"\\ud800"}'):
            with self.assertRaises(ValueError): c.parse(raw)
        self.assertEqual(c.adverse(b'{"nested":[{"category":"TRUST_BOUNDARY_DEFECT"}]}'),('ADVERSE',['category:TRUST_BOUNDARY_DEFECT']))
    def test_new_adverse_signals_block_invalid_retry(self):
        for value,signal in [({'gates':{'security':{'verdict':'N/A'}}},'security.verdict:N/A'),
                             ({'routing':'HARD_STOP'},'routing:HARD_STOP'),
                             ({'routing':'ESCALATE_FOUNDER'},'routing:ESCALATE_FOUNDER'),
                             ({'requires_human':True},'requires_human:true')]:
            with self.subTest(signal=signal):
                self.assertEqual(c.adverse(c.canon(value)),('ADVERSE',[signal]))
    def test_reserved_act_precedes_security_na_schema(self):
        vectors=json.loads((HERE/'CONFORMANCE-VECTORS-v0.1.json').read_text())
        result=next(x['instance'] for x in vectors['schema_cases'] if x['id']=='security-na-reserved-act')
        c.schema('review-result.schema.json',result)
        self.assertEqual(c.routing(result),('ESCALATE_FOUNDER',True))
    def test_shared_parser_publishes_reasoning_envelope(self):
        from provider_envelope import provider_response
        pub,run_dir=self.publisher_fixture()
        # Recreate the fixture using the same raw provider envelope in both consumers.
        raw=c.canon({'model':'claude-opus-5-5','stop_reason':'end_turn','content':[
            {'type':'thinking','thinking':'opaque','signature':'sig'},
            {'type':'redacted_thinking','data':'opaque'},
            {'type':'text','text':c.canon(self.result).decode()}]})
        adir=pathlib.Path(run_dir); record=c.parse((adir/'invocation-record.json').read_bytes())
        record['raw_output_sha256']=c.sha(raw);record['raw_output_bytes']=len(raw)
        record.pop('review_record_sha256'); record['review_record_sha256']=c.sha(c.canon({'packet_sha256':self.m['packet_sha256'],'result_sha256':record['result_sha256'],'invocation_record_without_hash':record}))
        for name,data in [('raw-response.json',raw),('invocation-record.json',c.canon(record))]:
            (adir/name).chmod(0o600);(adir/name).write_bytes(data)
        self.assertIs(pub.provider_response,provider_response)
        self.assertIs(inv.provider_response,provider_response)
        seen=[];pub.api=self.fake_app_api(seen)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),contextlib.redirect_stdout(io.StringIO()):pub.main()
        self.assertEqual((adir/'raw-response.json').read_bytes(),raw)
    def test_retained_release_selection_binds_historical_validators(self):
        pub,run_dir=self.publisher_fixture()
        old=self.work/'historical';(old/'bin').mkdir(parents=True)
        for name in ('runtime_contract.py','runtime_invoke.py'):
            data=subprocess.check_output(['git','show','1dfa5310228d8309c5450cf93a090c6d21b7b1ba:'+name],cwd=HERE)
            (old/'bin'/name).write_bytes(data)
        (old/'MANIFEST.sha256').write_bytes(b'pinned fixture manifest')
        recordpath=pathlib.Path(run_dir)/'invocation-record.json';record=c.parse(recordpath.read_bytes());record['attempt']=2
        recordpath.chmod(0o600);recordpath.write_bytes(c.canon(record))
        pub.RECOVERY_RELEASE_PATH=str(old);pub.RECOVERY_MANIFEST=c.sha(b'pinned fixture manifest');pub.RECOVERY_PACKET=self.m['packet_sha256']
        pub.select_retained_release(str(old),str(self.packet),run_dir)
        self.assertEqual(pub.TASK,str(old/'evaluator-task.md'))
        self.assertEqual(pub.adverse(b'{"requires_human":true}'),('NONE',[]))
        self.assertEqual(c.adverse(b'{"requires_human":true}'),('ADVERSE',['requires_human:true']))
        self.assertEqual(pub.schema.__globals__['HERE'],old/'bin')
        # Validate and publish a retained attempt with old scanner/image/scan bindings.
        import shutil
        for name in ('profile.json','evaluator-task.md','config.json','provider-terms.json','RUNTIME.json'):
            shutil.copyfile(self.release/name,old/name)
        shutil.copytree(HERE/'schemas',old/'schemas')
        pub.validate_packet.__globals__['read_root']=fixture_read
        pub.scan.__globals__['read_root']=fixture_read
        (old/'bin'/'foundry-packet-builder').write_bytes((HERE/'foundry-packet-builder').read_bytes())
        previous=copy.deepcopy(record);previous.update(attempt=1,result_sha256=None,schema_validation='INVALID_MALFORMED',routing_check='NOT_APPLICABLE',raw_output_sha256=c.sha(b'{}'),raw_output_bytes=2)
        previous.pop('review_record_sha256');previous['review_record_sha256']=c.sha(c.canon({'packet_sha256':self.m['packet_sha256'],'result_sha256':None,'invocation_record_without_hash':previous}))
        prevdir=pathlib.Path(run_dir); nextdir=prevdir.parent/'attempt-2';nextdir.mkdir()
        for name,data in [('raw-response.json',b'{}'),('invocation-record.json',c.canon(previous))]:
            (prevdir/name).chmod(0o600);(prevdir/name).write_bytes(data)
        self.result['gates']['security']={'verdict':'FAIL','finding_ids':['FND-SEC-001']}
        self.result.update(overall='FAIL',routing='HARD_STOP',requires_human=True,findings=[{'finding_id':'FND-SEC-001','gate':'security','severity':'MAJOR','category':'IMPLEMENTATION_DEFECT','title':'Unsafe retry','detail':'Retained failure','evidence_refs':[{'member':'files/a.md','line_start':1,'line_end':1}]}])
        record['result_sha256']=c.sha(c.canon(self.result))
        record['adverse_signal_scan']={'algorithm_version':'0.1','outcome':'ADVERSE','matched_signals':['verdict:FAIL']}
        raw=c.canon({'model':'claude-opus-5-5','stop_reason':'end_turn','content':[{'type':'thinking','thinking':'opaque','signature':'sig'},{'type':'text','text':c.canon(self.result).decode()}]})
        record['pre_transmission_disclosure']['scanner_sha256']=c.sha((old/'bin'/'runtime_invoke.py').read_bytes())
        record['environment']['runtime_image_sha256']=c.sha((old/'RUNTIME.json').read_bytes()+(old/'MANIFEST.sha256').read_bytes())
        record.update(raw_output_sha256=c.sha(raw),raw_output_bytes=len(raw))
        record.pop('review_record_sha256');record['review_record_sha256']=c.sha(c.canon({'packet_sha256':self.m['packet_sha256'],'result_sha256':record['result_sha256'],'invocation_record_without_hash':record}))
        for name,data in [('raw-response.json',raw),('invocation-record.json',c.canon(record)),('result.json',c.canon(self.result))]: (nextdir/name).write_bytes(data)
        pub.validate_evidence(str(self.packet),str(nextdir))
        seen=[];pub.api=self.fake_app_api(seen)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),str(nextdir)]),contextlib.redirect_stdout(io.StringIO()):pub.main()
        self.assertEqual((nextdir/'raw-response.json').read_bytes(),raw)
        self.assertEqual(next(x[2]['conclusion'] for x in seen if x[1].endswith('/check-runs')),'failure')
        self.assertEqual(next(x[2]['event'] for x in seen if x[1].endswith('/reviews')),'REQUEST_CHANGES')

    def test_malformed_reasoning_envelope_is_indeterminate(self):
        for block in ({'type':'thinking','thinking':None},{'type':'redacted_thinking','data':7}):
            with self.subTest(block=block),self.assertRaises(c.Reject):
                inv.provider_response(c.canon({'model':'claude-opus-5-5','stop_reason':'end_turn','content':[block,{'type':'text','text':'{}'}]}))
    def test_retained_release_rejects_unpinned_path_before_loading(self):
        pub,run_dir=self.publisher_fixture()
        with self.assertRaisesRegex(c.Reject,'unapproved evidence release'):
            pub.select_retained_release(str(self.release),str(self.packet),run_dir)
    def test_poll_requires_activation_authority(self):
        proc=subprocess.run([sys.executable,str(HERE/'foundry-evaluator-poll')],capture_output=True,text=True)
        self.assertNotEqual(proc.returncode,0)
        self.assertIn('no activation authority',proc.stderr)
    def test_publisher_revalidates_record_raw_context_and_routing(self):
        self.responses=[self.response()]; _,out=self.invoke()
        pub=load('foundry-evaluator-publish'); pub.PROFILE=str(self.release/'profile.json'); pub.TASK=str(self.release/'evaluator-task.md')
        pub.read_root_file=fixture_read
        pub.validate_evidence(str(self.packet),out['run_dir'])
        record_path=pathlib.Path(out['run_dir'])/'invocation-record.json'; record=c.parse(record_path.read_bytes()); record['tools_available']=['shell']; record_path.chmod(0o600); record_path.write_bytes(c.canon(record))
        with self.assertRaisesRegex(c.Reject,'context'): pub.validate_evidence(str(self.packet),out['run_dir'])
    def publisher_fixture(self):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        self.responses=[self.response()]; _,out=self.invoke()
        pub=load('foundry-evaluator-publish'); pub.PROFILE=str(self.release/'profile.json'); pub.TASK=str(self.release/'evaluator-task.md'); pub.read_root_file=fixture_read
        pub.verify_release=lambda p:None
        pub.APP_CONFIG=str(self.etc/'github-app.json'); pub.APP_KEY=str(self.etc/'github-app.pem')
        (self.etc/'github-app.json').write_bytes((HERE/'github-app.json').read_bytes())
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        (self.etc/'github-app.pem').write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        return pub,out['run_dir']
    def fake_app_api(self,seen,stale_after=None):
        def api(method,path,token,body=None):
            seen.append((method,path,body))
            perms={'checks':'write','contents':'read','pull_requests':'write','metadata':'read'}
            if path=='/app': return {'id':5263160,'slug':'foundry-evaluator'}
            if path=='/app/installations/169955633': return {'app_id':5263160,'permissions':perms,'repository_selection':'selected'}
            if path.endswith('/access_tokens'): return {'token':'app-installation-only','permissions':perms}
            if method=='GET':
                count=sum(x[0]=='GET' and '/pulls/' in x[1] for x in seen)
                return {'state':'open','head':{'sha':('f'*40 if stale_after and count>=stale_after else self.m['head_sha'])}}
            if path.endswith('/check-runs'): return {'id':101,'app':{'id':5263160},'head_sha':self.m['head_sha']}
            if path.endswith('/reviews'): return {'id':202,'commit_id':self.m['head_sha'],'user':{'login':'foundry-evaluator[bot]','type':'Bot'}}
            raise AssertionError(path)
        return api
    def test_app_bounded_token_pass_publication_and_idempotence(self):
        pub,run_dir=self.publisher_fixture(); seen=[]; pub.api=self.fake_app_api(seen)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),contextlib.redirect_stdout(io.StringIO()):
            pub.main(); posts=sum(x[0]=='POST' for x in seen); pub.main()
        self.assertEqual(sum(x[0]=='POST' and not x[1].endswith('/access_tokens') for x in seen),2)
        token=next(x for x in seen if x[1].endswith('/access_tokens'))
        self.assertEqual(token[2],{'repository_ids':[1297877588],'permissions':{'checks':'write','contents':'read','pull_requests':'write'}})
        check=next(x[2] for x in seen if x[1].endswith('/check-runs')); review=next(x[2] for x in seen if x[1].endswith('/reviews'))
        self.assertEqual(check['conclusion'],'success'); self.assertEqual(review['event'],'APPROVE')
        self.assertEqual(review['commit_id'],self.m['head_sha'])
        self.assertNotIn('private-session',review['body']); self.assertNotIn('host_id',review['body'])
    def test_stale_head_blocks_all_publication(self):
        pub,run_dir=self.publisher_fixture(); seen=[]; pub.api=self.fake_app_api(seen,stale_after=1)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),self.assertRaisesRegex(c.Reject,'stale'): pub.main()
        self.assertFalse(any(x[1].endswith(('/reviews','/check-runs')) for x in seen))
    def test_head_moves_between_check_and_review_preserves_uncertainty(self):
        pub,run_dir=self.publisher_fixture(); seen=[]; pub.api=self.fake_app_api(seen,stale_after=3)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),self.assertRaisesRegex(c.Reject,'stale'): pub.main()
        self.assertTrue((pathlib.Path(run_dir)/'publication/check.json').exists())
        self.assertFalse(any(x[1].endswith('/reviews') for x in seen))
        pub.api=self.fake_app_api(seen)
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),self.assertRaisesRegex(c.Reject,'uncertain'): pub.main()
    def test_app_permission_drift_refuses_token(self):
        pub,run_dir=self.publisher_fixture(); seen=[]; api=self.fake_app_api(seen)
        def drift(method,path,token,body=None):
            result=api(method,path,token,body)
            if path=='/app/installations/169955633': result['permissions']['contents']='write'
            return result
        pub.api=drift
        with patch.object(pub.sys,'argv',['publish',str(self.packet),run_dir]),self.assertRaisesRegex(c.Reject,'permission'): pub.main()
        self.assertFalse(any(x[0]=='POST' for x in seen))
    def test_controller_invalidity_publishes_action_required_without_gate_claims(self):
        pub,unused=self.publisher_fixture()
        self.members['files/a.md']=b'another packet\n'; self.m['changed_files'][0]['head_content_sha256']=c.sha(self.members['files/a.md']); self.m['changed_files'][0]['size']=len(self.members['files/a.md']); self.reseal()
        self.responses=[self.response('not json')]; rc,out=self.invoke(); self.assertEqual(rc,4)
        seen=[]; pub.api=self.fake_app_api(seen)
        with patch.object(pub.sys,'argv',['publish','--controller-stop',str(self.packet),out['run_dir']]),contextlib.redirect_stdout(io.StringIO()): pub.main()
        check=next(x[2] for x in seen if x[1].endswith('/check-runs')); review=next(x[2] for x in seen if x[1].endswith('/reviews'))
        self.assertEqual(check['conclusion'],'action_required'); self.assertEqual(review['event'],'REQUEST_CHANGES')
        self.assertIn('No valid gate verdicts',review['body']); self.assertNotIn('private-session',review['body'])
    def test_installed_release_drift_rejected(self):
        release=self.work/'frozen'; release.mkdir(); (release/'source').mkdir(); (release/'bin').mkdir()
        (release/'source/foundry-packet-builder').write_bytes(b'frozen')
        (release/'bin/foundry-packet-builder').write_bytes(b'changed')
        (release/'MANIFEST.sha256').write_text(c.sha(b'frozen')+'  foundry-packet-builder\n')
        with self.assertRaisesRegex(c.Reject,'installed release drift'): c.verify_release(release)
    def test_frozen_dependency_image_detects_changed_and_added_files(self):
        release=self.work/'image'; release.mkdir(); (release/'venv').mkdir()
        (release/'MANIFEST.sha256').write_bytes(b'')
        dep=release/'venv/library.py'; dep.write_bytes(b'frozen dependency')
        (release/'RUNTIME.json').write_bytes(c.canon({'venv/library.py':{'sha256':c.sha(dep.read_bytes())}}))
        c.verify_release(release)
        dep.write_bytes(b'changed dependency')
        with self.assertRaisesRegex(c.Reject,'dependency drift'): c.verify_release(release)
        dep.write_bytes(b'frozen dependency'); (release/'venv/injection.pth').write_bytes(b'unexpected')
        with self.assertRaisesRegex(c.Reject,'file set drift'): c.verify_release(release)
    def test_root_custody_rejects_user_owned_input(self):
        original_read=REAL_READ
        if os.getuid()!=0:
            with self.assertRaises(c.Reject): original_read(self.packet/'manifest.json')
        path=self.work/'link'; path.symlink_to(self.packet/'manifest.json')
        with self.assertRaises(Exception): original_read(path)
    def runner_fixture(self):
        runner=load('foundry-evaluator-run')
        runner.ROOT=str(self.work/'controller'); runner.REPO=str(self.work/'repo.git'); pathlib.Path(runner.REPO).mkdir()
        runner.RELEASE=self.release; runner.PROFILE=str(self.release/'profile.json'); runner.BUILDER=str(HERE/'foundry-packet-builder')
        runner.verify_release=lambda p:None; runner.read_root=fixture_read
        pr={'state':'open','head':{'sha':self.m['head_sha'],'repo':{'id':1297877588}},'base':{'sha':self.m['base_sha'],'ref':'main','repo':{'id':1297877588}}}
        runner.api=lambda path:copy.deepcopy(pr)
        def run(cmd,check=True):
            if cmd[0]==runner.BUILDER:
                target=pathlib.Path(cmd[cmd.index('--output')+1]); __import__('shutil').copytree(self.packet,target)
                return subprocess.CompletedProcess(cmd,0,json.dumps({'packet_sha256':self.m['packet_sha256'],'packet_dir':str(target)}),'')
            if 'rev-parse' in cmd: return subprocess.CompletedProcess(cmd,0,self.m['head_sha']+'\n','')
            if 'merge-base' in cmd: return subprocess.CompletedProcess(cmd,0,self.m['merge_base_sha']+'\n','')
            if 'fetch' in cmd: return subprocess.CompletedProcess(cmd,0,'','')
            raise AssertionError('seal-only must never invoke or publish: '+repr(cmd))
        runner.run=run
        return runner,pr
    def test_seal_only_is_idempotent_and_cannot_invoke_or_publish(self):
        runner,pr=self.runner_fixture()
        with patch.object(runner.sys,'argv',['runner','26','--seal-only',self.m['base_sha'],self.m['head_sha']]),contextlib.redirect_stdout(io.StringIO()) as out:
            runner.main(); first=json.loads(out.getvalue()); out.seek(0); out.truncate(0); runner.main(); second=json.loads(out.getvalue())
        self.assertEqual(first,second); self.assertEqual(first['status'],'SEALED')
        self.assertEqual(pathlib.Path(first['packet_dir']).stat().st_mode&0o777,0o500)
        self.assertEqual((pathlib.Path(first['packet_dir'])/'manifest.json').stat().st_mode&0o777,0o400)
    def test_moved_head_during_seal_retains_staging_and_build_evidence(self):
        runner,pr=self.runner_fixture(); count=0
        def moved(path):
            nonlocal count
            count+=1; value=copy.deepcopy(pr)
            if count>=2: value['head']['sha']='f'*40
            return value
        runner.api=moved
        with patch.object(runner.sys,'argv',['runner','26','--seal-only',self.m['base_sha'],self.m['head_sha']]),self.assertRaisesRegex(SystemExit,'moved'): runner.main()
        self.assertTrue(list(pathlib.Path(runner.ROOT).glob('staging/*/manifest.json')))
        self.assertTrue(list(pathlib.Path(runner.ROOT).glob('heads/**/build-*/status.json')))
        self.assertFalse(list(pathlib.Path(runner.ROOT).glob('heads/**/sealed.json')))

if __name__=='__main__': unittest.main()
