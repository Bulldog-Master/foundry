import hashlib, json, os, subprocess, sys, tempfile, threading, shutil, uuid, http.server, re
import jsonschema
HERE=os.path.dirname(os.path.abspath(__file__)); SCH=os.path.abspath(os.path.join(HERE,"..","schemas"))
sha=lambda b:hashlib.sha256(b).hexdigest()
jcs=lambda o:json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
W=tempfile.mkdtemp(); ETC=W+"/etc"; RUNS=W+"/runs"; os.makedirs(ETC); os.makedirs(RUNS)
TASK=b"TASK v0.1\n"; open(ETC+"/evaluator-task.md","wb").write(TASK)
open(ETC+"/config.json","w").write(json.dumps({"model":"claude-opus-5-5","max_tokens":32000,"effort":"medium"}))
open(ETC+"/api-key","w").write("sk-ant-TESTKEY\n")
QUEUE=[]; SEEN=[]
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(s):
        n=int(s.headers["content-length"]); body=s.rfile.read(n); SEEN.append((s.headers.get("x-api-key"),json.loads(body)))
        st,out=QUEUE.pop(0); s.send_response(st); s.send_header("request-id","req_test"); s.send_header("content-type","application/json"); s.end_headers(); s.wfile.write(out)
    def log_message(*a): pass
srv=http.server.HTTPServer(("127.0.0.1",0),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
code=open(HERE+"/foundry-evaluator-invoke").read()
for a,b in [('ETC = "/etc/foundry-evaluator"','ETC = %r'%ETC),('RUNS = "/var/lib/foundry-evaluator/runs"','RUNS = %r'%RUNS),('"https://api.anthropic.com/v1/messages"','"http://127.0.0.1:%d/v1/messages"'%srv.server_port)]:
    assert a in code; code=code.replace(a,b)
open(W+"/inv.py","w").write(code)
G="b"*40
def make_packet(content=b"hello\n"):
    d=tempfile.mkdtemp(dir=W); os.makedirs(d+"/files"); os.makedirs(d+"/gov")
    mem={"diff.patch":b"diff --git a/a.md b/a.md\n"+content,"files/a.md":content,"gov/ADR.md":b"adr\n"}
    for n,b in mem.items(): open(d+"/"+n,"wb").write(b)
    m={"packet_schema_version":"0.1","packet_id":str(uuid.uuid4()),"repository":{"owner":"o","name":"r","repo_id":1},"pr_number":26,"base_ref":"main","base_sha":G,"merge_base_sha":G,"head_repository":{"owner":"o","name":"r","repo_id":1},"head_sha":"c"*40,
     "changed_files":[{"path":"a.md","status":"added","mode":"100644","head_blob_sha":G,"head_content_sha256":sha(mem["files/a.md"]),"size":len(content),"member":"files/a.md"}],
     "diff":{"member":"diff.patch","sha256":sha(mem["diff.patch"]),"git_version":"2.43.0","flags":["--binary"]},
     "governance_refs":[{"path":"adrs/ADR.md","role":"governing","source_sha":G,"sha256":sha(mem["gov/ADR.md"]),"member":"gov/ADR.md"}],
     "evaluator_task":{"task_id":"four-gate","version":"0.1","sha256":sha(TASK)},"allowed_context":["pr_diff"],"prohibited_context":["network_access"],
     "review_round":{"round":1,"prior_packet_sha256":None,"prior_findings":[]},"producer_identity":{"component":"foundry-packet-builder","version":"0.1","build_sha256":"a"*64},
     "completeness":{"complete":True,"truncated":False,"size_bytes":10,"size_limit_bytes":100},
     "members":[{"name":n,"sha256":sha(b),"size":len(b)} for n,b in mem.items()],"packet_created_at":"2026-10-09T23:00:00Z"}
    m["packet_sha256"]=sha(jcs(m)); open(d+"/manifest.json","w").write(json.dumps(m)); return d,m
def result(m,**kw):
    r={"result_schema_version":"0.1","packet_sha256":m["packet_sha256"],"pr_number":26,"head_sha":m["head_sha"],"evaluator_task_sha256":m["evaluator_task"]["sha256"],
       "gates":{g:{"verdict":"PASS","finding_ids":[]} for g in ("architecture","security","privacy","quality")},"findings":[],"overall":"PASS","routing":"CONTINUE","requires_human":False}
    r.update(kw); return r
def api(text): return (200,json.dumps({"id":"m","type":"message","model":"claude-opus-5-5-20260101","content":[{"type":"text","text":text}],"stop_reason":"end_turn"}).encode())
def run(d): 
    p=subprocess.run([sys.executable,"-I",W+"/inv.py",d],capture_output=True,text=True); return p.returncode,p.stdout,p.stderr
fails=[]
def check(name,cond):
    print(("PASS " if cond else "FAIL ")+name); 
    if not cond: fails.append(name)
# 1 valid
d,m=make_packet(); QUEUE.append(api(json.dumps(result(m))))
rc,o,e=run(d); check("1 valid PASS -> exit 0",rc==0); check("1 key sent, no tools in request",SEEN[-1][0]=="sk-ant-TESTKEY" and "tools" not in SEEN[-1][1])
check("1 effective token and effort controls sent",SEEN[-1][1]["max_tokens"]==32000 and SEEN[-1][1]["output_config"]=={"effort":"medium"})
ad=RUNS+"/"+m["packet_sha256"]+"/attempt-1"
meta=json.load(open(ad+"/request-meta.json")); check("1 request metadata records controls",meta["max_tokens"]==32000 and meta["effort"]=="medium")
rec=json.load(open(ad+"/invocation-record.json")); jsonschema.Draft202012Validator(json.load(open(SCH+"/invocation-record.schema.json"))).validate(rec); check("1 invocation record validates against schema",True)
jsonschema.Draft202012Validator(json.load(open(SCH+"/review-result.schema.json"))).validate(json.load(open(ad+"/result.json"))); check("1 result validates against schema",True)
check("1 key not in any output file", all(b"TESTKEY" not in open(os.path.join(ad,f),"rb").read() for f in os.listdir(ad)))
rc,o,e=run(d); check("2 valid result never re-run -> exit 4",rc==4)
# 3 malformed then valid then refused
d,m=make_packet(b"b\n"); QUEUE.append(api("not json")); rc,o,e=run(d); check("3a malformed -> exit 5",rc==5)
QUEUE.append(api(json.dumps(result(m)))); rc,o,e=run(d); check("3b second attempt valid -> exit 0",rc==0)
rc,o,e=run(d); check("3c third refused -> exit 4",rc==4)
# 4 both malformed
d,m=make_packet(b"c\n"); QUEUE.append(api("x")); run(d); QUEUE.append(api("{}")); rc,o,e=run(d); check("4a second malformed -> exit 5",rc==5)
rc,o,e=run(d); check("4b hard stop refuses -> exit 4","HARD_STOP" in e and rc==4)
# 5 tampered member
d,m=make_packet(b"d\n"); open(d+"/files/a.md","ab").write(b"x"); rc,o,e=run(d); check("5 tampered member rejected -> exit 2",rc==2 and "mismatch" in e)
# 5b extra file, symlink
d,m=make_packet(b"e\n"); open(d+"/extra.txt","w").write("x"); rc,o,e=run(d); check("5b unlisted file rejected",rc==2)
d,m=make_packet(b"f\n"); os.symlink("/etc/passwd",d+"/link"); rc,o,e=run(d); check("5c symlink rejected",rc==2)
# 5d manifest altered (packet hash)
d,m=make_packet(b"g\n"); m2=dict(m); m2["pr_number"]=27; open(d+"/manifest.json","w").write(json.dumps(m2)); rc,o,e=run(d); check("5d altered manifest rejected",rc==2)
# 6 routing mismatch: FAIL finding but routing CONTINUE
d,m=make_packet(b"h\n"); r=result(m); r["gates"]["security"]={"verdict":"FAIL","finding_ids":["FND-SEC-001"]}; r["overall"]="FAIL"
r["findings"]=[{"finding_id":"FND-SEC-001","gate":"security","category":"IMPLEMENTATION_DEFECT","severity":"MAJOR","title":"t","evidence_refs":[{"path":"a.md","line_start":1,"line_end":1}]}]
QUEUE.append(api(json.dumps(r))); rc,o,e=run(d); check("6a wrong routing -> MISMATCH exit 5",rc==5 and "MISMATCH" in o)
r["routing"]="RETURN_TO_OPERATIONS"; QUEUE.append(api(json.dumps(r))); rc,o,e=run(d); check("6b correct routing on attempt 2 -> exit 0",rc==0 and "RETURN_TO_OPERATIONS" in o)
# 7 transport error does not consume attempt
d,m=make_packet(b"i\n"); QUEUE.append((500,b"{}")); rc,o,e=run(d); check("7a HTTP 500 -> exit 3",rc==3)
QUEUE.append(api(json.dumps(result(m)))); rc,o,e=run(d); check("7b retry after transport error is attempt 1",rc==0 and '"attempt": 1' in o)
# 8 binding mismatch
d,m=make_packet(b"j\n"); r=result(m); r["head_sha"]="d"*40; QUEUE.append(api(json.dumps(r))); rc,o,e=run(d); check("8 head_sha mismatch -> INVALID_BINDING_MISMATCH",rc==5 and "INVALID_BINDING_MISMATCH" in o)
# 9 evidence path outside packet; PASS gate carrying findings; prose wrapped JSON; max_tokens stop
d,m=make_packet(b"k\n"); r=result(m); r["gates"]["security"]={"verdict":"FAIL","finding_ids":["FND-SEC-001"]}; r["overall"]="FAIL"; r["routing"]="RETURN_TO_OPERATIONS"
r["findings"]=[{"finding_id":"FND-SEC-001","gate":"security","category":"IMPLEMENTATION_DEFECT","severity":"MAJOR","title":"t","evidence_refs":[{"path":"nope.md","line_start":1,"line_end":1}]}]
QUEUE.append(api(json.dumps(r))); rc,o,e=run(d); check("9a evidence path outside packet rejected",rc==5 and "evidence path" in o)
QUEUE.append(api("Here is my review:\n"+json.dumps(result(m)))); rc,o,e=run(d); check("9b prose-wrapped JSON is malformed (no repair)",rc==5)
d,m=make_packet(b"l\n"); QUEUE.append((200,json.dumps({"model":"x","content":[{"type":"text","text":json.dumps(result(m))}],"stop_reason":"max_tokens"}).encode())); rc,o,e=run(d); check("9c truncated (max_tokens) is malformed",rc==5)
# 10 task hash mismatch
d,m=make_packet(b"m\n"); open(ETC+"/evaluator-task.md","wb").write(b"CHANGED"); rc,o,e=run(d); check("10 task hash mismatch rejected",rc==2 and "task hash" in e); open(ETC+"/evaluator-task.md","wb").write(TASK)
print("\nFAILED:",fails if fails else "none"); sys.exit(1 if fails else 0)
