#!/usr/bin/env python3
"""
PDF → Audiobook (Clean MP3 Chapters @ 192 kbps) — neat from the start

Features
- Robust chapter parsing: deduplicates by chapter number; removes heading lines from body.
- Female voice by default (edge-tts). If online TTS is blocked, falls back to offline (pyttsx3 on Windows).
- MP3 @ exact bitrate via FFmpeg when present (recommended). If missing, WAV is kept.
- Skip existing: by default, won't re-synthesize chapters that already have MP3s.
- ID3 tags: Title=chapter title, Album=PDF name (or --album), Artist=voice (or --artist), Track=chapter number.
- Optional ZIP bundling (N chapters per part).

Usage example
  python make_audiobook.py --pdf "Input/book.pdf" --out "Output/book" --bitrate 192k --zip_chunk 3

Personal use only. Respect copyright.
"""

import argparse
import asyncio
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Tuple, List

from PyPDF2 import PdfReader
import edge_tts
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

try:
    from aiohttp.client_exceptions import WSServerHandshakeError
except Exception:
    class WSServerHandshakeError(Exception):
        pass

# ================== Parsing helpers ==================

CHAP_RE = re.compile(r'^Chapter\s+(\d+)\s*[:：]?\s*(.*)$', re.IGNORECASE)

NOISE_PATTERNS = [
    r'^\s*OceanofPDF\.com\s*$',
    r'^https?://\S+$',
    r'^\s*Routledge\s*$',
    r'^\s*Taylor\s*&\s*Francis.*$',
    r'^\s*Library of Congress.*$',
]

def _clean_line(line: str) -> str:
    s = line.strip()
    if not s:
        return ""
    if CHAP_RE.match(s):
        return ""  # drop headings from body
    for pat in NOISE_PATTERNS:
        if re.match(pat, s):
            return ""
    return s

def detect_chapters(pdf_path: Path) -> Dict[int, Dict[str, str]]:
    """
    Return {chapter_number: {"title": "Chapter N: Title", "text": "..."}}
    where 0 is Front Matter.
    """
    reader = PdfReader(str(pdf_path))
    chapters: Dict[int, Dict[str, str]] = {0: {"title": "Front Matter", "text": ""}}
    current = 0

    for page in reader.pages:
        text = page.extract_text() or ""
        lines = text.splitlines()

        # capture headings (may be multiple per page)
        page_nums: List[int] = []
        for raw in lines:
            m = CHAP_RE.match(raw.strip())
            if m:
                num = int(m.group(1))
                name = (m.group(2) or "").strip()
                title = f"Chapter {num}: {name}" if name else f"Chapter {num}"
                if num not in chapters:
                    chapters[num] = {"title": title, "text": ""}
                else:
                    # prefer longer/more specific title
                    old = chapters[num]["title"]
                    old_short = old.replace(f"Chapter {num}:", "").strip()
                    if name and len(name) > len(old_short):
                        chapters[num]["title"] = title
                page_nums.append(num)

        if page_nums:
            current = page_nums[-1]

        body = "\n".join([_clean_line(ln) for ln in lines if _clean_line(ln)])
        if body:
            chapters[current]["text"] += body + "\n"

    return chapters

def pretty_filename(ch_num: int, title: str) -> Tuple[str, str]:
    if ch_num == 0:
        return f"{0:02d}_Front_Matter.mp3", "Front Matter"
    m = CHAP_RE.match(title)
    if m:
        num = int(m.group(1))
        name = (m.group(2) or "").strip() or f"Chapter {num}"
        safe = re.sub(r'[^A-Za-z0-9_]+', '_', name).strip('_')
        return f"{num:02d}_{safe}.mp3", f"Chapter {num}: {name}"
    safe = re.sub(r'[^A-Za-z0-9_]+', '_', title).strip('_')
    return f"{ch_num:02d}_{safe}.mp3", title

def split_chunks(text: str, max_chars: int = 2800) -> List[str]:
    paras = re.split(r"\n{2,}", text)
    chunks: List[str] = []
    cur = ""
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p) if cur else p
        else:
            if cur:
                chunks.append(cur)
            if len(p) <= max_chars:
                cur = p
            else:
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i:i+max_chars])
                cur = ""
    if cur:
        chunks.append(cur)
    return chunks

def _escape_ssml(text: str) -> str:
    return text.replace("&", " and ").replace("<", " ").replace(">", " ")

# ================== TTS helpers ==================

async def tts_online_to_mp3(ssml: str, out_tmp_mp3: Path, voice: str):
    communicate = edge_tts.Communicate(text=ssml, voice=voice)
    await communicate.save(str(out_tmp_mp3))

def select_offline_voice(engine, prefer=("Zira", "Jenny", "Aria", "Hazel", "Samantha", "Eva")):
    try:
        for v in engine.getProperty("voices"):
            nm = getattr(v, "name", "")
            if any(p.lower() in nm.lower() for p in prefer):
                engine.setProperty("voice", v.id)
                return
        vs = engine.getProperty("voices")
        if vs:
            engine.setProperty("voice", vs[0].id)
    except Exception:
        pass

def tts_offline_to_wav(full_text: str, wav_path: Path):
    import pyttsx3
    eng = pyttsx3.init()
    try:
        rate = eng.getProperty("rate")
        eng.setProperty("rate", int(rate * 0.95))
    except Exception:
        pass
    select_offline_voice(eng)
    eng.save_to_file(full_text, str(wav_path))
    eng.runAndWait()

def ffmpeg_on_path() -> bool:
    return shutil.which("ffmpeg") is not None

def convert_wav_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str) -> bool:
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav_path), "-codec:a", "libmp3lame", "-b:a", bitrate, str(mp3_path)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except Exception:
        return False

def tag_mp3(mp3_path: Path, title: str, album: str, artist: str, track_num: int):
    try:
        try:
            audio = EasyID3(str(mp3_path))
        except ID3NoHeaderError:
            audio = EasyID3()
        audio["title"] = title
        audio["album"] = album
        audio["artist"] = artist
        audio["tracknumber"] = str(track_num)
        audio.save(str(mp3_path))
    except Exception:
        # non-fatal
        pass

# ================== Core synthesis ==================

async def tts_chapter(text: str, out_mp3: Path, voice: str, spoken_title: str, pause_ms: int, bitrate: str,
                      album: str, artist: str, track_num: int) -> None:
    tmp_online = out_mp3.with_suffix(".raw.mp3")
    try:
        tmp_online.unlink(missing_ok=True)
    except Exception:
        pass

    # Build SSML
    parts = [f'<speak version="1.0" xml:lang="en-US"><voice name="{voice}"><p><s>{spoken_title}</s></p><break time="{pause_ms}ms"/>' ]
    for chunk in split_chunks(text):
        parts.append(f'<p>{_escape_ssml(chunk)}</p><break time="{pause_ms}ms"/>')
    parts.append("</voice></speak>")
    ssml = "".join(parts)

    # Try online first
    did_online = False
    try:
        await tts_online_to_mp3(ssml, tmp_online, voice)
        did_online = True
    except (WSServerHandshakeError,) as e:
        print(f"[WARN] Online TTS blocked/refused. Falling back to offline. Detail: {e}")
    except Exception as e:
        print(f"[WARN] Online TTS failed: {e}. Falling back to offline.")

    if did_online and tmp_online.exists():
        # enforce bitrate or keep as-is
        if ffmpeg_on_path():
            ok = convert_wav_to_mp3(tmp_online, out_mp3, bitrate)  # this call accepts mp3-in too
            if ok:
                tmp_online.unlink(missing_ok=True)
            else:
                tmp_online.rename(out_mp3)
        else:
            tmp_online.rename(out_mp3)
        tag_mp3(out_mp3, spoken_title, album, artist, track_num)
        return

    # Offline fallback → WAV then convert to MP3 if ffmpeg
    wav_path = out_mp3.with_suffix(".wav")
    full_text = f"{spoken_title}.  {text}"
    tts_offline_to_wav(full_text, wav_path)

    if ffmpeg_on_path():
        ok = convert_wav_to_mp3(wav_path, out_mp3, bitrate)
        if ok:
            wav_path.unlink(missing_ok=True)
            tag_mp3(out_mp3, spoken_title, album, artist, track_num)
            return
        else:
            print("[WARN] ffmpeg conversion failed; keeping WAV.")
    else:
        print("[INFO] ffmpeg not found; keeping WAV.")

# ================== ZIP bundling ==================

def bundle_zip(out_dir: Path, zip_chunk: int) -> None:
    mp3s = sorted([p for p in out_dir.glob("*.mp3")])
    if zip_chunk <= 0 or not mp3s:
        return
    import zipfile
    for i in range(0, len(mp3s), zip_chunk):
        batch = mp3s[i:i+zip_chunk]
        zpath = out_dir / f"audiobook_part_{i//zip_chunk + 1:02d}.zip"
        with zipfile.ZipFile(zpath, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for f in batch:
                zf.write(f, arcname=f.name)

# ================== CLI ==================

async def main():
    ap = argparse.ArgumentParser(description="PDF → Audiobook (clean MP3 chapters @192k)")
    ap.add_argument("--pdf", required=True, help="Path to source PDF")
    ap.add_argument("--out", default="audiobook_output", help="Output folder")
    ap.add_argument("--voice", default="en-US-JennyNeural", help="edge-tts voice (female by default)")
    ap.add_argument("--bitrate", default="192k", help="MP3 bitrate (requires ffmpeg). Example: 192k")
    ap.add_argument("--pause_ms", type=int, default=600, help="Pause between sections (ms)")
    ap.add_argument("--zip_chunk", type=int, default=3, help="Chapters per ZIP (0 to disable)")
    ap.add_argument("--skip_existing", action="store_true", default=True, help="Skip chapters with existing MP3")
    ap.add_argument("--overwrite", action="store_true", help="Force re-synthesis (disables skip_existing)")
    ap.add_argument("--album", default="", help="Album tag (default: PDF file name without extension)")
    ap.add_argument("--artist", default="", help="Artist tag (default: voice name)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    album = args.album.strip() or pdf_path.stem
    artist = args.artist.strip() or args.voice

    print(f"[INFO] Parsing chapters from: {pdf_path.name}")
    chapters = detect_chapters(pdf_path)

    ordered = sorted(chapters.keys())
    if 0 in ordered:
        ordered.remove(0)
        ordered = [0] + ordered

    print(f"[INFO] Found {len(ordered)} sections")
    for idx, ch_num in enumerate(ordered):
        title = chapters[ch_num]["title"]
        text = chapters[ch_num]["text"].strip()
        fname, spoken = pretty_filename(ch_num, title)
        out_mp3 = out_dir / fname
        track = ch_num  # reasonable track = chapter number

        if args.overwrite:
            pass  # always regenerate
        elif args.skip_existing and out_mp3.exists():
            print(f"[SKIP] {spoken} (existing MP3)")
            continue

        if ch_num != 0 and not text:
            print(f"[WARN] Empty text for {title}; skipping.")
            continue

        print(f"[SAY] {spoken} → {fname}")
        await tts_chapter(text=text, out_mp3=out_mp3, voice=args.voice, spoken_title=spoken,
                          pause_ms=args.pause_ms, bitrate=args.bitrate, album=album, artist=artist, track_num=track)

        # Clean up any intermediates if MP3 exists
        if out_mp3.exists():
            raw = out_mp3.with_suffix(".raw.mp3")
            wav = out_mp3.with_suffix(".wav")
            raw.unlink(missing_ok=True)
            wav.unlink(missing_ok=True)

    if args.zip_chunk > 0:
        bundle_zip(out_dir, args.zip_chunk)

    print(f"[DONE] Files saved in: {out_dir}")

if __name__ == "__main__":
    asyncio.run(main())
