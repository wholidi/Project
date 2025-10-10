# 🪔 Hindi PDF → Audiobook Converter

Convert Hindi (or bilingual) PDF documents into **high-quality MP3 audiobooks**, powered by **Microsoft Edge TTS** (for natural voice) and **pyttsx3** (for offline fallback).

---

## 🎯 Key Features

| Feature | Description |
|----------|--------------|
| 🇮🇳 **Hindi Language Support** | Reads both **Hindi (Devanagari)** and **English** text smoothly |
| 🗣️ **Localized Voices** | Default: `hi-IN-SwaraNeural` (female), optional: `hi-IN-MadhurNeural` (male) |
| 🧾 **Smart Chapter Detection** | Detects both `Chapter 1` and `अध्याय १` / `भाग 2` headings |
| 🔠 **Devanagari Digit Handling** | Automatically converts `०१२३४५६७८९` → `0123456789` |
| 🎧 **High-Quality MP3 Output** | 192kbps audio with FFmpeg (if installed) |
| 💬 **Offline Fallback** | Uses `pyttsx3` voices when internet is unavailable |
| 🗂️ **Auto Bundling** | Groups every 3 chapters into ZIPs for easy sharing |
| 🧱 **Self-contained Setup** | No manual Python setup needed — just run one `.bat` file |

---

## 🛠️ Quick Start

### Option 1: Use the All-in-One Batch File (Recommended)

1. Place your **Hindi PDFs** inside the `Input\` folder.  
2. Double-click:  
   ```bash
   ALLPDFS_hindi_FIX_NEW.bat
   ```
3. Output will be created in:
   ```bash
   Output_HI\<BookName>\
   ```

🪶 The script will:
- Create a local virtual environment `.venv_hindi`
- Install all required libraries (`PyPDF2`, `edge-tts`, `mutagen`, `pyttsx3`)
- Generate MP3 files chapter by chapter
- Bundle them into ZIPs

---

### Option 2: Run the Python Script Directly

```bash
python make_audiobook_hi_FIXED.py --pdf "Input/book_hi.pdf" --out "Output_HI/book_hi"
```

**Optional arguments:**

| Argument | Default | Description |
|-----------|----------|-------------|
| `--voice` | `hi-IN-SwaraNeural` | Choose Edge TTS voice |
| `--lang` | `hi-IN` | Set SSML language tag |
| `--bitrate` | `192k` | MP3 bitrate (requires ffmpeg) |
| `--zip_chunk` | `3` | Chapters per ZIP bundle |
| `--skip_existing` | `True` | Skip already-processed chapters |
| `--overwrite` | `False` | Reprocess all chapters |
| `--pause_ms` | `600` | Pause between sections (milliseconds) |

---

## 📦 Requirements

To install dependencies manually:
```bash
pip install -r requirements_hindi_audiobook.txt
```

**requirements_hindi_audiobook.txt**
```txt
PyPDF2>=3.0.0
edge-tts>=6.1.0
mutagen>=1.47.0
pyttsx3>=2.90
```

---

## 💡 Notes

- Ensure **FFmpeg** is installed and available in your PATH for proper MP3 conversion.  
  Download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- The script automatically skips blank pages or watermark lines (e.g., *OceanofPDF*, *Routledge*).
- Works best on structured PDFs with text layers (not scanned images).

---

## 🧰 Folder Structure

```
📂 Hindi_Audiobook_Converter/
 ├── Input/                     ← Drop all Hindi PDFs here
 ├── Output_HI/                 ← Generated MP3s & ZIPs
 ├── make_audiobook_hi_FIXED.py ← Main script
 ├── ALLPDFS_hindi_FIX_NEW.bat  ← One-click runner
 ├── requirements_hindi_audiobook.txt
 └── README_Hindi.md            ← This file
```

---

## 🪷 Example Output

```
Output_HI/
 ├── MyHindiBook/
 │   ├── 00_प्राक्कथन.mp3
 │   ├── 01_अध्याय_1_परिचय.mp3
 │   ├── 02_भाग_2_इतिहास.mp3
 │   ├── audiobook_part_01.zip
 │   └── ...
```

---

## 🔄 Comparison with English Version

| Feature | English Version | Hindi Version |
|----------|-----------------|----------------|
| Default Voice | `en-US-JennyNeural` | `hi-IN-SwaraNeural` |
| Chapter Regex | `Chapter 1:` | `Chapter 1:`, `अध्याय १:`, `भाग 2:` |
| Localized Speech | ❌ | ✅ |
| Digit Handling | ❌ | ✅ |
| SSML Tag | `en-US` | `hi-IN` |
| Self-Installer Batch | Basic | Full auto-setup |
| Fallback Voice | English only | Hindi + English mixed |

---

## 🧑‍💻 Author

**Developed by:** [William Hartono (wholidi)](https://wholidi.github.io)  
🌐 [https://wholidi.github.io](https://wholidi.github.io)  
🪩 AI Audit & Governance | Ethical AI | Digital Transformation

---

> _Build Trust. Ensure Compliance. Unlock Responsible AI._
