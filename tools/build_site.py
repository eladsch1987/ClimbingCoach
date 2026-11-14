"""Build the static site for Vercel: wraps the artifact pages in a full HTML document and copies assets to site/."""
import os, shutil, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#0B7A63">\n<link rel="manifest" href="manifest.json">\n<link rel="apple-touch-icon" href="icon.png">\n<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n'
NAV = '<nav style="display:flex;gap:16px;justify-content:center;padding:10px 16px;font:600 14px Inter,system-ui,sans-serif;background:var(--bg,#f1f4f3)"><a href="index.html" style="color:var(--work,var(--accent,#0B7A63))">Timer</a><a href="guide.html" style="color:var(--work,var(--accent,#0B7A63))">Exercise guide</a></nav>\n'
def wrap(src, dst):
    s = open(os.path.join(ROOT, src), encoding="utf-8").read()
    m = re.search(r"<title>.*?</title>", s, re.S)
    title = m.group(0) if m else "<title>Climbing Coach</title>"
    body = s.replace(title, "", 1)
    # move <style> and <link>/<meta> tags into head
    head_bits = "".join(re.findall(r"<link[^>]*>|<meta[^>]*>|<style>.*?</style>", body, re.S))
    body = re.sub(r"<link[^>]*>|<meta[^>]*>|<style>.*?</style>", "", body, flags=re.S)
    open(os.path.join(OUT, dst), "w", encoding="utf-8").write(HEAD + title + "\n" + head_bits + "\n</head>\n<body>\n" + NAV + body + "\n</body>\n</html>\n")
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
wrap("workout-timer.html", "index.html")
wrap("exercise-guide.html", "guide.html")
for d in ["anim", "images", "audio/cues"]:
    shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d), ignore=shutil.ignore_patterns("*.md", "*.json", "PROMPTS*"))
shutil.copy(os.path.join(ROOT, "anim", "rest.jpg"), os.path.join(OUT, "icon.png"))
open(os.path.join(OUT, "manifest.json"), "w").write('{"name":"Climbing Coach","short_name":"Coach","start_url":"index.html","display":"standalone","background_color":"#F1F4F3","theme_color":"#0B7A63","icons":[{"src":"icon.png","sizes":"512x512","type":"image/jpeg"}]}')
print("built", sorted(os.listdir(OUT)))
