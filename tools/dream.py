"""Small driver for dreamina-canvas: create image nodes, confirm credits, run, wait, download."""
import json,subprocess,random,sys,time,os
P="d4b8f86e-5963-4298-ade9-e6b8932bd97b"
STATE="images/dreamina-state.json"
A="0123456789abcdefghjkmnpqrstvwxyz"
def nid(): return "node_"+"".join(random.choice(A) for _ in range(10))
def dc(*args):
    r=subprocess.run(["dreamina-canvas",*args,"--project-id",P,"--yes","--non-interactive"],capture_output=True,text=True)
    try: return json.loads(r.stdout)
    except Exception: return {"ok":False,"raw":(r.stdout+r.stderr)[:800]}
def load(): return json.load(open(STATE))
def save(d): json.dump(d,open(STATE,"w"),indent=1)
def create(title,prompt,refs):
    n=nid(); args=["node","create","image","--node-id",n,"--title",title,"--mode","i2i","--model","seedream_5.5","--ratio","4:3","--resolution","1.5K","--count","1","--prompt",prompt]
    for r in refs: args+=["--ref",r]
    out=dc(*args)
    if not out.get("ok"): print("CREATE FAIL",title,out); return None
    st=load(); st[title]={"nodeId":n,"prompt":prompt}; save(st); return n
def run(titles):
    import uuid
    for b in range(0,len(titles),13):
        batch=titles[b:b+13]; st=load(); nodes=[st[t]["nodeId"] for t in batch]
        nargs=sum([["--node-id",n] for n in nodes],[])
        q=dc("node","quote",*nargs); ceiling=q["data"]["totalMaxCredits"]
        c=dc("node","confirm","--credit-ceiling",str(ceiling),*nargs)
        tok=c.get("data",{}).get("creditConfirmationToken")
        if not tok: print("CONFIRM?",json.dumps(c)[:600])
        subs=[]
        for t in batch:
            s_=str(uuid.uuid4()); st[t]["submitId"]=s_; subs+=["--submit-id",s_]
        save(st)
        args=["node","run",*nargs,*subs]+(["--credit-token",tok] if tok else [])
        r=dc(*args); print("RUN", "ok" if r.get("ok") else json.dumps(r)[:600], "credits",ceiling)
def wait_dl(titles,outdir):
    st=load(); pending=set(titles); t0=time.time()
    while pending and time.time()-t0<900:
        for t in list(pending):
            r=dc("node","show","--node-id",st[t]["nodeId"])
            try: node=r["data"]["nodes"][0]["node"]
            except Exception: print("show err",t,str(r)[:300]); continue
            ress=[x for x in node.get("resources",[]) if x.get("submitId")==st[t].get("submitId")] or node.get("resources",[])
            if node["status"] in ("failed","error") or (ress and ress[-1]["status"] in ("failed","error")):
                print("FAILED",t,json.dumps(node)[:500]); st[t]["state"]="failed"; pending.discard(t); continue
            if ress and ress[-1]["status"]=="success":
                res=ress[-1]["resourceId"]; st[t]["resourceId"]=res; st[t]["state"]="succeeded"
                d=dc("resource","download",res,"--output",f"{outdir}/{t}.png")
                print("OK",t,"dl" if d.get("ok") else d); pending.discard(t)
        save(st)
        if pending: time.sleep(10)
    if pending: print("pending",pending)
