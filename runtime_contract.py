"""Frozen controller validation. Subject-repository code is never imported."""
import hashlib
import json
import os
import pathlib
import re
import stat
from jsonschema import Draft202012Validator, FormatChecker

HERE = pathlib.Path(__file__).resolve().parent
SCHEMAS = HERE / 'schemas' if (HERE / 'schemas').is_dir() else HERE.parent / 'schemas'
ALLOWED = ['packet_manifest', 'packet_members', 'evaluator_task']
ROUTING = 'foundry-routing-v0.1-security-na-hard-stop'
PREFIX = {'architecture':'ARCH', 'security':'SEC', 'privacy':'PRIV', 'quality':'QUAL'}
HARD = {'TRUST_BOUNDARY_DEFECT','INTEGRITY_ANOMALY','SPEC_AMBIGUITY','OTHER'}

class Reject(ValueError): pass

def sha(data): return hashlib.sha256(data).hexdigest()

def canon(value):
    def check(x):
        if isinstance(x, str):
            if any(0xd800 <= ord(c) <= 0xdfff for c in x): raise Reject('surrogate')
        elif isinstance(x, dict):
            for k, v in x.items(): check(k); check(v)
        elif isinstance(x, list):
            for v in x: check(v)
        elif x is None or isinstance(x, bool): pass
        elif isinstance(x, int) and -(2**53)+1 <= x <= (2**53)-1: pass
        else: raise Reject('unsupported number')
    check(value)
    return json.dumps(value, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode('utf-8')

def parse(raw):
    def pairs(rows):
        out = {}
        for k, v in rows:
            if k in out: raise Reject('duplicate key')
            out[k] = v
        return out
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(Reject('non-JSON constant')))
    canon(value)
    return value

def read_root(path, limit=8_000_000):
    path = pathlib.Path(path)
    for parent in path.parents:
        s = parent.lstat()
        if stat.S_ISLNK(s.st_mode): raise Reject('symlink ancestor')
        # /tmp is allowed only as the system-owned sticky staging parent.
        if s.st_uid != 0 or (s.st_mode & 0o022 and not s.st_mode & stat.S_ISVTX):
            raise Reject('unsafe ancestor')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if not stat.S_ISREG(s.st_mode) or s.st_uid != 0 or s.st_mode & 0o022:
            raise Reject('unsafe owner/mode')
        with os.fdopen(fd, 'rb') as f:
            fd = -1
            data = f.read(limit+1)
        if len(data) > limit: raise Reject('oversized file')
        return data
    finally:
        if fd != -1: os.close(fd)

def schema(name, value):
    canon(value)
    Draft202012Validator(json.loads((SCHEMAS / name).read_text()), format_checker=FormatChecker()).validate(value)

def routing(r):
    cats = {f['category'] for f in r['findings']}
    if 'RESERVED_ACT_REQUIRED' in cats: return 'ESCALATE_FOUNDER', True
    if r['gates']['security']['verdict'] in ('FAIL','N/A'): return 'HARD_STOP', True
    if cats & HARD or any(f['severity']=='CRITICAL' for f in r['findings']): return 'HARD_STOP', True
    if any(g['verdict'] in ('FAIL','PASS_WITH_CONDITIONS') for g in r['gates'].values()): return 'RETURN_TO_OPERATIONS', False
    return 'CONTINUE', False

def validate_result(r, m, members):
    schema('review-result.schema.json', r)
    for key in ('packet_sha256','head_sha','pr_number'):
        if r[key] != m[key]: raise Reject('binding mismatch')
    if r['evaluator_task_sha256'] != m['evaluator_task']['sha256'] or r['routing_profile'] != ROUTING:
        raise Reject('task binding mismatch')
    indexed = [i for g in r['gates'].values() for i in g['finding_ids']]
    actual = [f['finding_id'] for f in r['findings']]
    if len(set(indexed)) != len(indexed) or len(set(actual)) != len(actual) or sorted(indexed) != sorted(actual):
        raise Reject('finding index')
    for f in r['findings']:
        if not f['finding_id'].startswith('FND-'+PREFIX[f['gate']]+'-') or f['finding_id'] not in r['gates'][f['gate']]['finding_ids']:
            raise Reject('finding gate prefix/index')
        for e in f['evidence_refs']:
            if e['member'] not in members: raise Reject('evidence member')
            count = len(members[e['member']].decode('utf-8').splitlines()) or 1
            if not 1 <= e['line_start'] <= e['line_end'] <= count: raise Reject('evidence line range')
    vs = [g['verdict'] for g in r['gates'].values()]
    expected = 'FAIL' if 'FAIL' in vs else 'PASS_WITH_CONDITIONS' if 'PASS_WITH_CONDITIONS' in vs else 'PASS'
    if r['overall'] != expected: raise Reject('derived overall')
    if (r['routing'],r['requires_human']) != routing(r): raise Reject('routing mismatch')

def adverse(raw):
    try:
        value = parse(raw)
        if not isinstance(value, dict): raise Reject('non-object')
    except (ValueError, UnicodeError): return 'INDETERMINATE', []
    signals = set()
    def walk(x):
        if isinstance(x, dict):
            for key, choices in [('verdict',{'FAIL'}),('severity',{'CRITICAL'}),('category',HARD|{'RESERVED_ACT_REQUIRED'})]:
                if isinstance(x.get(key), str) and x[key] in choices: signals.add(key+':'+x[key])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(value)
    return ('ADVERSE' if signals else 'NONE'), sorted(signals)

def validate_packet(directory, profile, task):
    directory = pathlib.Path(directory)
    m = parse(read_root(directory/'manifest.json'))
    schema('review-packet.schema.json',m)
    body = dict(m); declared = body.pop('packet_sha256')
    if sha(canon(body)) != declared: raise Reject('packet hash')
    if sha(canon(profile)) != m['governance_profile_sha256']: raise Reject('profile hash')
    if m['evaluator_task'] != profile['evaluator_task'] or sha(task) != m['evaluator_task']['sha256']: raise Reject('task hash')
    if m['repository'] != profile['repository'] or m['head_repository'] != profile['head_repository']: raise Reject('repository binding')
    if m['producer_identity']['build_sha256']!=sha(read_root(HERE/'foundry-packet-builder')): raise Reject('builder binding')
    declared_members = {}
    for row in m['members']:
        name = row['name']
        if not name or name == 'manifest.json' or name.startswith('/') or any(p in ('','..','.') for p in name.split('/')) or name in declared_members:
            raise Reject('unsafe/duplicate member')
        declared_members[name] = row
    disk = set()
    for root, dirs, files in os.walk(directory,followlinks=False):
        for name in dirs+files:
            if os.path.islink(os.path.join(root,name)): raise Reject('packet symlink')
        for name in files: disk.add(str(pathlib.Path(root,name).relative_to(directory)))
    if disk != set(declared_members)|{'manifest.json'}: raise Reject('packet member set')
    members = {}
    for name,row in declared_members.items():
        data = read_root(directory/name,4_000_000)
        data.decode('utf-8') # This commissioning release explicitly rejects binary input.
        if len(data) != row['size'] or sha(data) != row['sha256']: raise Reject('member hash/size')
        members[name] = data
    total = sum(map(len,members.values()))
    if total != m['completeness']['size_bytes'] or total > min(4_000_000,m['completeness']['size_limit_bytes']): raise Reject('packet size')
    def link(row,key):
        if row['member'] not in declared_members or declared_members[row['member']]['sha256'] != row[key]: raise Reject('member cross-reference')
    link(m['diff'],'sha256')
    for row in m['changed_files']:
        if row['status'] != 'deleted':
            link(row,'head_content_sha256')
            if row['size'] != declared_members[row['member']]['size']: raise Reject('changed size')
    governing = [r for r in m['governance_refs'] if r['role']=='governing']
    subject = [r for r in m['governance_refs'] if r['role']=='subject_head_version']
    expected_subject = list(dict.fromkeys(profile['subject_at_head']+[r['path'] for r in m['changed_files'] if r['path'] in profile['governing_at_base']]))
    if [r['path'] for r in governing] != profile['governing_at_base'] or [r['path'] for r in subject] != expected_subject: raise Reject('governing paths')
    for row in m['governance_refs']:
        link(row,'sha256')
        if row['source_sha'] != m['base_sha' if row['role']=='governing' else 'head_sha']: raise Reject('governing source')
    observed = []
    for row in m['related_context_refs']:
        link(row,'sha256')
        if row['source_sha'] != m[row['source']+'_sha']: raise Reject('context source')
        observed.append({k:row[k] for k in ('path','source','gates','justification')})
    if observed != profile['related_context']: raise Reject('context profile')
    return m,members

def put(directory,name,data):
    fd = os.open(pathlib.Path(directory)/name, os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
    with os.fdopen(fd,'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())

def verify_release(release):
    """Check installed runtime copies against the externally pinned source manifest."""
    release=pathlib.Path(release)
    rows=read_root(release/'MANIFEST.sha256').decode().splitlines()
    for row in rows:
        digest,name=row.split('  ',1)
        source=release/'source'/name
        if sha(read_root(source))!=digest: raise Reject('frozen source drift: '+name)
        if name.startswith('schemas/'): installed=release/name
        elif name in ('runtime_contract.py','runtime_invoke.py') or name.startswith('foundry-') and '.' not in name:
            installed=release/'bin'/name
        elif name=='bootstrap0b-profile.json': installed=release/'profile.json'
        elif name in ('config.json','evaluator-task.md','provider-terms.json'): installed=release/name
        else: continue
        if sha(read_root(installed))!=digest: raise Reject('installed release drift: '+name)
    image=parse(read_root(release/'RUNTIME.json'))
    actual={str(p.relative_to(release)) for p in (release/'venv').rglob('*')
            if (p.is_file() or p.is_symlink()) and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if actual!=set(image): raise Reject('runtime dependency file set drift')
    for name,row in image.items():
        path=release/name
        if path.is_symlink():
            if os.readlink(path)!=row.get('symlink'): raise Reject('runtime symlink drift')
            path=path.resolve()
            if path.is_dir(): continue
        if sha(read_root(path,100_000_000))!=row['sha256']: raise Reject('runtime dependency drift: '+name)
