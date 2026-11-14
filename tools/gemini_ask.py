import json,sys,subprocess,time
def ask(prompt, url=None, images=None, models=("gemini-3.8-flash","gemini-3.5-flash-lite")):
    content=[{"type":"text","text":prompt}]
    if url: content.append({"type":"image_url","image_url":{"url":url}})
    for im in images or []:
        import base64; b=base64.b64encode(open(im,"rb").read()).decode()
        content.append({"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+b}})
    for m in models:
        for t in range(2):
            r=subprocess.run(["curl","-sS","https://generativelanguage.googleapis.com/v1beta/openai/chat/completions","-H","Authorization: Bearer proxy-injected","-H","Content-Type: application/json","-d",json.dumps({"model":m,"messages":[{"role":"user","content":content}]})],capture_output=True,text=True)
            try:
                d=json.loads(r.stdout)
                if isinstance(d,dict) and "choices" in d: return m, d["choices"][0]["message"]["content"]
            except Exception: d=r.stdout
            time.sleep(5)
    return None, str(d)[:400]
if __name__=="__main__":
    m,a=ask(open(sys.argv[1]).read(), url=sys.argv[2] if len(sys.argv)>2 else None); print("MODEL",m); print(a)
