# Audiobook Maker — neat from the start

This version gives you **clean MP3s @ 192 kbps** (with chapter titles and ID3 tags), dedupes/cleans headings, and **skips existing chapters** on re-run.

## Install
```bash
pip install -r requirements.txt
# Recommended: install FFmpeg and ensure it's on PATH so MP3s are created directly
# Windows quick: winget install Gyan.FFmpeg
```

## Run (single PDF)
```bash
python make_audiobook.py \
  --pdf "Input/YourBook.pdf" \
  --out "Output/YourBook" \
  --voice "en-US-JennyNeural" \
  --bitrate "192k" \
  --pause_ms 600 \
  --zip_chunk 3 \
  --skip_existing
```

**Flags**
- `--skip_existing` (default): don’t redo chapters that already have MP3s.
- `--overwrite`: force re-synthesis (disables skip).
- `--album`: MP3 album tag (default: PDF filename).
- `--artist`: MP3 artist tag (default: voice name).

If the online voice is blocked, the script falls back to **offline** (SAPI) and will create **WAVs** unless FFmpeg is available to convert to MP3.

## Run (all PDFs under Input → Output/<name>)
Use the Windows launcher provided in this bundle.
