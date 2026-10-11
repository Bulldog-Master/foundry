#!/usr/bin/env python3
import contextlib, importlib.machinery, io, json, os, pathlib, tempfile, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

HERE = pathlib.Path(__file__).resolve().parent
PUBLISHER = str(HERE / "foundry-evaluator-publish")
PACKET = "/unused/packet"
RUN = "/unused/run"
SCHEMAS = str(HERE / "schemas")
SEEN = []

class Handler(BaseHTTPRequestHandler):
    def _body(self):
        n=int(self.headers.get("content-length","0")); return json.loads(self.rfile.read(n) or b"{}")
    def _send(self,obj):
        b=json.dumps(obj).encode(); self.send_response(200); self.send_header("content-type","application/json"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        SEEN.append(("GET",self.path,None,self.headers.get("Authorization")))
        self._send({"state":"open","head":{"sha":"7af1d692f0f43d11c5ec92dab9d3ed913262ab7a"}})
    def do_POST(self):
        body=self._body(); SEEN.append(("POST",self.path,body,self.headers.get("Authorization")))
        if self.path.endswith("/access_tokens"): self._send({"token":"installation-token"})
        elif self.path.endswith("/check-runs"): self._send({"id":101})
        elif self.path.endswith("/reviews"): self._send({"id":202})
        else: self.send_error(404)
    def log_message(self,*args): pass

def main():
    m=importlib.machinery.SourceFileLoader("publisher",PUBLISHER).load_module()
    work=tempfile.mkdtemp(prefix="foundry-publisher-test-")
    key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    key_path=work+"/app.pem"; cfg_path=work+"/app.json"
    open(key_path,"wb").write(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.TraditionalOpenSSL,serialization.NoEncryption()))
    open(cfg_path,"w").write(json.dumps({"app_id":1,"installation_id":2,"repository_id":1297877588,"owner":"Bulldog-Master","repo":"foundry"}))
    os.chmod(key_path,0o600); os.chmod(cfg_path,0o600)
    def read_fixture_owner(path,*_):
        st=os.stat(path,follow_symlinks=False)
        if st.st_uid != os.getuid() or st.st_mode & 0o022: raise m.Reject("unsafe owner/mode: "+path)
        return open(path,"rb").read()
    m.read_root_file=read_fixture_owner
    server=HTTPServer(("127.0.0.1",0),Handler); threading.Thread(target=server.serve_forever,daemon=True).start()
    m.APP_KEY=key_path; m.APP_CONFIG=cfg_path; m.SCHEMA_DIR=SCHEMAS; m.API="http://127.0.0.1:%d"%server.server_port
    head="7af1d692f0f43d11c5ec92dab9d3ed913262ab7a"
    manifest={"repository":{"owner":"Bulldog-Master","name":"foundry","repo_id":1297877588},
              "pr_number":26,"head_sha":head,"packet_sha256":"a"*64}
    result={"head_sha":head,"overall":"FAIL","routing":"HARD_STOP","requires_human":True,
            "gates":{name:{"verdict":"FAIL"} for name in ("architecture","security","privacy","quality")},
            "findings":[]}
    m.validate_evidence=lambda packet,run:(manifest,result,{},"b"*64,"c"*64)
    m.sys.argv=[PUBLISHER,PACKET,RUN]
    out=io.StringIO()
    with contextlib.redirect_stdout(out): m.main()
    result=json.loads(out.getvalue())
    token_call=next(x for x in SEEN if x[1].endswith("/access_tokens"))
    check_call=next(x for x in SEEN if x[1].endswith("/check-runs"))
    review_call=next(x for x in SEEN if x[1].endswith("/reviews"))
    assert token_call[2]=={"repository_ids":[1297877588],"permissions":{"checks":"write","contents":"read","pull_requests":"write"}}
    assert check_call[2]["conclusion"]=="failure" and check_call[2]["head_sha"]=="7af1d692f0f43d11c5ec92dab9d3ed913262ab7a"
    assert review_call[2]["event"]=="REQUEST_CHANGES" and review_call[2]["commit_id"]=="7af1d692f0f43d11c5ec92dab9d3ed913262ab7a"
    assert result["check_run_id"]==101 and result["review_id"]==202
    print("PASS publisher requests bounded token, checks current head, and publishes FAIL as failure/REQUEST_CHANGES")

if __name__=="__main__": main()
