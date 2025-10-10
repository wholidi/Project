#!/usr/bin/env python3
"""
PDF → Audiobook (Hindi) — FIXED VERSION
- Fixes: f-strings, chapter dict init, regex braces, safe filenames, robust chapter parsing
- Keeps online (edge-tts) first; falls back to offline (pyttsx3) if needed.
"""
import argparse, asyncio, re, shutil, subprocess, sys
from pathlib import Path
from typing import Dict, Tuple, List
from PyPDF2 import PdfReader
import edge_tts
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

DEV_TO_ARABIC = str.maketrans("०१२३४५६७८९","0123456789")
def dev_to_int(s:str)->int:
    s=(s or "").strip().translate(DEV_TO_ARABIC)
    try: return int(s)
    except: return 0

CHAP_EN_RE = re.compile(r'^\s*Chapter\s+(\d+)\s*[:：]?\s*(.*)$', re.IGNORECASE)
CHAP_HI_RE = re.compile(r'^\s*(अध्याय|भाग)\s+([०-९\d]+)\s*[:：]?\s*(.*)$')

NOISE_PATTERNS = [
    r'^\s*OceanofPDF\.com\s*$',
    r'^https?://\S+$',
    r'^\s*Routledge\s*$',
    r'^\s*Taylor\s*&\s*Francis.*$',
    r'^\s*Library of Congress.*$'
]

def _clean_line(line:str)->str:
    s=(line or "").strip()
    if not s: return ""
    if CHAP_EN_RE.match(s) or CHAP_HI_RE.match(s): return ""
    for pat in NOISE_PATTERNS:
        if re.match(pat,s): return ""
    return s

def detect_chapters(pdf_path:Path)->Dict[int,Dict[str,str]]:
    r=PdfReader(str(pdf_path))
    chapters = {0: {"title":"Front Matter","text":""}}
    current=0
    for page in r.pages:
        text=page.extract_text() or ""
        lines=text.splitlines()
        page_nums=[]
        for raw in lines:
            raw_s=raw.strip()
            m_en=CHAP_EN_RE.match(raw_s)
            if m_en:
                num=int(m_en.group(1)); name=(m_en.group(2) or "").strip()
                title=f"Chapter {num}: {name}" if name else f"Chapter {num}"
                chapters.setdefault(num, {"title":title,"text":""})
                page_nums.append(num); continue
            m_hi=CHAP_HI_RE.match(raw_s)
            if m_hi:
                label=m_hi.group(1); num=dev_to_int(m_hi.group(2)); name=(m_hi.group(3) or "").strip()
                title=f"{label} {num}: {name}" if name else f"{label} {num}"
                chapters.setdefault(num, {"title":title,"text":""})
                page_nums.append(num); continue
        if page_nums: current=page_nums[-1]
        body="\n".join([_clean_line(ln) for ln in lines if _clean_line(ln)])
        if body: chapters[current]["text"]+=body+"\n"
    return chapters

def pretty_filename(ch_num:int,title:str,lang:str)->Tuple[str,str]:
    is_hi=lang.lower().startswith("hi")
    if ch_num==0:
        spoken="प्राक्कथन" if is_hi else "Front Matter"
        return f"{0:02d}_Front_Matter.mp3", spoken

    m_en=CHAP_EN_RE.match(title or "")
    if m_en:
        num=int(m_en.group(1)); name=(m_en.group(2) or "").strip() or f"Chapter {num}"
        import re as _re
        safe=_re.sub(r'[^A-Za-z0-9_]+','_',name).strip('_') or f"Chapter_{num}"
        spoken=(f"अध्याय {num}: {name}" if is_hi else f"Chapter {num}: {name}")
        return f"{num:02d}_{safe}.mp3", spoken

    m_hi=CHAP_HI_RE.match(title or "")
    if m_hi:
        label=m_hi.group(1); num=dev_to_int(m_hi.group(2)); name=(m_hi.group(3) or "").strip() or f"{label} {num}"
        import re as _re
        safe=_re.sub(r'[^A-Za-z0-9_]+','_',name).strip('_') or f"Adhyay_{num}"
        spoken=f"{label} {num}: {name}" if is_hi else f"Chapter {num}: {name}"
        return f"{num:02d}_{safe}.mp3", spoken

    import re as _re
    safe=_re.sub(r'[^A-Za-z0-9_]+','_', (title or f"Section_{ch_num}")).strip('_')
    spoken= title or (f"खंड {ch_num}" if is_hi else f"Section {ch_num}")
    return f"{ch_num:02d}_{safe}.mp3", spoken

def split_chunks(text:str,max_chars:int=2800):
    import re as _re
    paras=_re.split(r"\n{2,}",text)
    chunks=[]; cur=""
    for p in paras:
        p=p.strip()
        if not p: continue
        if len(cur)+len(p)+2<=max_chars:
            cur=(cur+"\n\n"+p) if cur else p
        else:
            if cur: chunks.append(cur)
            if len(p)<=max_chars: cur=p
            else:
                for i in range(0,len(p),max_chars): chunks.append(p[i:i+max_chars])
                cur=""
    if cur: chunks.append(cur)
    return chunks

def _escape_ssml(t:str)->str:
    return t.replace("&"," और ").replace("<"," ").replace(">"," ")

async def tts_online_to_mp3(ssml:str,out_tmp_mp3:Path,voice:str):
    communicate=edge_tts.Communicate(text=ssml,voice=voice)
    await communicate.save(str(out_tmp_mp3))

def select_offline_voice(engine, prefer=("Swara","Madhur","Hindi","hi-IN","Zira","Jenny","Aria")):
    try:
        for v in engine.getProperty("voices"):
            nm=getattr(v,"name","")
            if any(p.lower() in (nm or "").lower() for p in prefer):
                engine.setProperty("voice",v.id); return
        vs=engine.getProperty("voices")
        if vs: engine.setProperty("voice",vs[0].id)
    except: pass

def tts_offline_to_wav(full_text:str,wav_path:Path):
    import pyttsx3
    eng=pyttsx3.init()
    try:
        rate=eng.getProperty("rate"); eng.setProperty("rate", int(rate*0.95))
    except: pass
    select_offline_voice(eng)
    eng.save_to_file(full_text, str(wav_path)); eng.runAndWait()

def ffmpeg_on_path()->bool:
    return shutil.which("ffmpeg") is not None

def transcode_to_mp3(input_path:Path, mp3_path:Path, bitrate:str)->bool:
    """Transcodes any input audio readable by ffmpeg into MP3 @ bitrate."""
    try:
        subprocess.run(
            ["ffmpeg","-y","-i",str(input_path),"-codec:a","libmp3lame","-b:a",bitrate,str(mp3_path)],
            check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
        )
        return True
    except Exception as e:
        print(f"[WARN] ffmpeg transcode failed: {e}")
        return False

def tag_mp3(mp3_path:Path,title:str,album:str,artist:str,track_num:int):
    try:
        try: audio=EasyID3(str(mp3_path))
        except ID3NoHeaderError: audio=EasyID3()
        audio["title"]=title; audio["album"]=album; audio["artist"]=artist; audio["tracknumber"]=str(track_num)
        audio.save(str(mp3_path))
    except: pass

async def tts_chapter(text:str,out_mp3:Path,voice:str,spoken_title:str,pause_ms:int,bitrate:str,album:str,artist:str,track_num:int,lang:str):
    tmp=out_mp3.with_suffix(".tmp.mp3")
    try: tmp.unlink(missing_ok=True)
    except: pass

    parts=[f'<speak version="1.0" xml:lang="{lang}"><voice name="{voice}"><p><s>{spoken_title}</s></p><break time="{pause_ms}ms"/>' ]
    for chunk in split_chunks(text):
        parts.append(f'<p>{_escape_ssml(chunk)}</p><break time="{pause_ms}ms"/>' )
    parts.append("</voice></speak>"); ssml="".join(parts)

    did_online=False
    try:
        await tts_online_to_mp3(ssml,tmp,voice); did_online=True
    except Exception as e:
        print(f"[WARN] Online TTS failed: {e}. Falling back to offline.")

    if did_online and tmp.exists():
        # Edge-tts already outputs mp3; only transcode if you insist on exact bitrate
        if ffmpeg_on_path():
            ok=transcode_to_mp3(tmp,out_mp3,bitrate)
            if ok: tmp.unlink(missing_ok=True)
            else: tmp.rename(out_mp3)
        else: tmp.rename(out_mp3)
        tag_mp3(out_mp3,spoken_title,album,artist,track_num); return

    # Offline fallback produces WAV then (optionally) MP3
    wav=out_mp3.with_suffix(".wav")
    full=f"{spoken_title}.  {text}"; tts_offline_to_wav(full,wav)
    if ffmpeg_on_path():
        ok=transcode_to_mp3(wav,out_mp3,bitrate)
        if ok: wav.unlink(missing_ok=True); tag_mp3(out_mp3,spoken_title,album,artist,track_num); return
        else: print("[WARN] ffmpeg conversion failed; keeping WAV.")
    else: print("[INFO] ffmpeg not found; keeping WAV.]")

def bundle_zip(out_dir:Path, zip_chunk:int):
    mp3s=sorted([p for p in out_dir.glob("*.mp3")])
    if zip_chunk<=0 or not mp3s: return
    import zipfile
    for i in range(0,len(mp3s),zip_chunk):
        batch=mp3s[i:i+zip_chunk]
        zpath=out_dir/f"audiobook_part_{i//zip_chunk + 1:02d}.zip"
        with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED) as zf:
            for f in batch: zf.write(f, arcname=f.name)

async def main():
    ap=argparse.ArgumentParser(description="PDF → Audiobook (Hindi, clean MP3 chapters @192k)")
    ap.add_argument("--pdf", required=True, help="Path to a single PDF file")
    ap.add_argument("--out", default="audiobook_output_hi", help="Output directory")
    ap.add_argument("--voice", default="hi-IN-SwaraNeural")
    ap.add_argument("--lang", default="hi-IN")
    ap.add_argument("--bitrate", default="192k")
    ap.add_argument("--pause_ms", type=int, default=600)
    ap.add_argument("--zip_chunk", type=int, default=3)
    ap.add_argument("--skip_existing", action="store_true", help="Skip chapters if MP3 already exists")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing MP3s")
    ap.add_argument("--album", default="")
    ap.add_argument("--artist", default="")
    args=ap.parse_args()

    pdf_path=Path(args.pdf).expanduser().resolve()
    out_dir=Path(args.out).expanduser().resolve(); out_dir.mkdir(parents=True, exist_ok=True)
    album=args.album.strip() or pdf_path.stem; artist=args.artist.strip() or args.voice

    print(f"[INFO] Parsing chapters from: {pdf_path.name}")
    chapters=detect_chapters(pdf_path)
    ordered=sorted(chapters.keys())
    if 0 in ordered: ordered.remove(0); ordered=[0]+ordered
    print(f"[INFO] Found {len(ordered)} sections")

    for ch in ordered:
        title=chapters[ch]["title"]; text=chapters[ch]["text"].strip()
        fname,spoken=pretty_filename(ch,title,args.lang); out_mp3=out_dir/fname; track=ch

        if args.overwrite:
            pass
        elif args.skip_existing and out_mp3.exists():
            print(f"[SKIP] {spoken} (existing MP3)"); continue

        if ch!=0 and not text:
            print(f"[WARN] Empty text for {title}; skipping."); continue

        print(f"[SAY] {spoken} → {fname}")
        await tts_chapter(
            text=text,
            out_mp3=out_mp3,
            voice=args.voice,
            spoken_title=spoken,
            pause_ms=args.pause_ms,
            bitrate=args.bitrate,
            album=album,
            artist=artist,
            track_num=track,
            lang=args.lang
        )
        if out_mp3.exists():
            for ext in (".tmp.mp3",".wav"):
                p=out_mp3.with_suffix(ext); 
                try: p.unlink(missing_ok=True)
                except: pass

    if args.zip_chunk>0: bundle_zip(out_dir,args.zip_chunk)
    print(f"[DONE] Files saved in: {out_dir}")

if __name__=="__main__":
    asyncio.run(main())
