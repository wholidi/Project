# Audiobook Maker — PDF → Clean MP3 Chapters (Windows)

Convert any PDF into a chapterized **audiobook** with a **female voice**, tidy filenames, and **ID3 tags** — all from the command line on Windows.

> ⚠️ **Copyright**: Only convert content you have the rights to use (your work, public domain, or with permission).

---

## ✨ Features
- **Neat output**: one MP3 per chapter (e.g., `01_Introduction.mp3`) — intermediates auto‑deleted.
- **Robust chapter parser**: deduplicates by chapter number and strips headings/footers.
- **Voice**: Microsoft neural voice via `edge-tts` (online).
  - **Automatic offline fallback** to Windows SAPI (`pyttsx3`) if the online service is blocked.
- **Exact MP3 bitrate** with **FFmpeg** (recommended). If FFmpeg is missing during offline mode, WAVs are kept.
- **Skip existing** chapters on re‑run (fast resumes). Use `--overwrite` when you want to re‑synthesize.
- **ID3 tags** per chapter: Title (chapter), Album (book), Artist (voice), Track (chapter number).
- **Optional ZIPs**: bundle N chapters per ZIP (for easy transfer to players).

---

## 🧰 Requirements
- **Windows 10/11**
- **Python 3.9+**
- **FFmpeg** (recommended for MP3 @ 192 kbps)
  ```powershell
  winget install Gyan.FFmpeg
  ```
  Restart your terminal and verify: `ffmpeg -version`.

---

## 📦 Install
```powershell
# from the repo or bundle folder
py -m pip install -r .\requirements.txt
```
> The Windows launcher also runs this for you automatically on first use.

---

## 🚀 Quick start (Windows)
1. Put your PDFs in `Input\`.
2. Double‑click **`run_ALLPDFS_neat.bat`**.

Each book will be written to `Output\<PDFName>\` as **clean MP3 chapters** (plus optional ZIPs).

### Run the script directly (for one file / custom flags)
```powershell
py .\make_audiobook.py ^
  --pdf ".\Input\YourBook.pdf" ^
  --out ".\Output\YourBook" ^
  --voice "en-US-JennyNeural" ^
  --bitrate "192k" ^
  --pause_ms 600 ^
  --zip_chunk 3 ^
  --skip_existing
```

---

## ⚙️ Options
```text
--pdf            Path to source PDF  (required)
--out            Output folder (default: audiobook_output)
--voice          edge-tts voice (default: en-US-JennyNeural)
--bitrate        MP3 bitrate (needs ffmpeg, default: 192k)
--pause_ms       Pause between sections in ms (default: 600)
--zip_chunk      Chapters per ZIP bundle (0 = disable, default: 3)
--skip_existing  Skip chapters that already have MP3s (default: on)
--overwrite      Force re-synthesis (disables skip_existing)
--album          MP3 album tag (default: PDF filename without extension)
--artist         MP3 artist tag (default: voice name)
```

**Examples**
- Change voice: `--voice "en-US-AriaNeural"`
- Disable ZIPs: `--zip_chunk 0`
- Redo everything: add `--overwrite`

---

## 🧠 How it works
1. **Parse chapters** — detect headings like `Chapter 1`, `Chapter 2`, …  
   Deduplicate by chapter number and remove heading lines from narration.
2. **Synthesize** — online with `edge-tts` (neural). If blocked, auto‑fallback to offline SAPI (`pyttsx3`).
3. **Encode** — if FFmpeg is available, produce **MP3 @ 192 kbps** and delete `.wav/.raw`. Otherwise, WAV is kept for offline mode.
4. **Tag** — apply ID3 tags (Title/Album/Artist/Track) to each MP3.
5. **Bundle** — optionally ZIP chapters in parts.

---

## 📁 Folder layout
```
repo/
├─ Input/                        # drop your PDFs here
├─ Output/
│  └─ YourBook/                  # clean MP3s per chapter (+ optional ZIPs)
├─ make_audiobook.py             # main script
├─ run_ALLPDFS_neat.bat          # Windows launcher (all PDFs in Input)
├─ requirements.txt
└─ README.md
```

---

## 🌐 Network notes
If you see a `WSServerHandshakeError 403` from `edge-tts`, your network is blocking the Microsoft speech service (`wss://speech.platform.bing.com`). The script **automatically falls back** to offline SAPI. To regain neural voice later, try from home/hotspot or ask IT to allow that domain.

---

## 🛠 Troubleshooting
- **Only WAV files appear** → Install FFmpeg and reopen PowerShell; re‑run.
- **`py` not recognized** → use `python` in place of `py`.
- **Dependency warnings** → generally safe to ignore for this tool.
- **Re‑processing everything** → `--skip_existing` is enabled by default. Delete only the chapters you want to redo, or pass `--overwrite`.

---

## 🧾 License
MIT (or your preferred license). Be sure to respect copyright law where you live.

---

## 🙏 Acknowledgements
- [edge-tts](https://pypi.org/project/edge-tts/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [mutagen](https://pypi.org/project/mutagen/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [FFmpeg](https://ffmpeg.org/)
