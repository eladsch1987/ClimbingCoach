"""Split each voice cue into chunks under 4.8 s, cut in pauses.
Why: Chrome on Android gives clips shorter than 5 s only *temporary* audio focus,
so Spotify ducks and comes back by itself; a 12 s clip takes full focus and Spotify stays paused."""
import subprocess,re,json,glob,os
MAX=4.8
def silences(f,d):
    out=subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af",f"silencedetect=noise=-35dB:d={d}","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
    return [(a+b)/2 for a,b in zip(st,en)]
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
man={}
for old in glob.glob("audio/cues/parts/*.mp3"): os.remove(old)
for f in sorted(glob.glob("audio/cues/*.mp3")):
    k=os.path.basename(f)[:-4]; D=dur(f)
    cuts=sorted(set(silences(f,0.25)+silences(f,0.12)))
    pts=[0.0]
    while D-pts[-1]>MAX:
        ok=[c for c in cuts if pts[-1]+0.8<c<=pts[-1]+MAX]
        pts.append(max(ok) if ok else pts[-1]+MAX)
    if D-pts[-1]<0.4 and len(pts)>1: pass  # tail is just silence: drop it
    else: pts.append(D)
    n=len(pts)-1
    for i in range(n):
        subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-ss",f"{pts[i]:.3f}","-to",f"{pts[i+1]:.3f}","-c:a","libmp3lame","-q:a","4",f"audio/cues/parts/{k}_{i+1}.mp3"],check=True)
    man[k]=n; print(k,n,[round(p,2) for p in pts])
json.dump(man,open("audio/cues/parts/manifest.json","w"))
