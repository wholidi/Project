@echo off
setlocal EnableExtensions
chcp 65001 >NUL
echo === USING UPDATED ALLPDFS_hindi_FIX_NEW.bat ===

REM --- Base paths (adjust if your folder names differ) ---
set "BASE=%~dp0"
set "VENV=%BASE%.venv_hindi\Scripts\activate.bat"
set "REQ=%BASE%requirements_hindi_audiobook.txt"
set "PYFIX=%BASE%make_audiobook_hi_FIXED.py"
set "INPUT=%BASE%Input"
set "OUTPUT=%BASE%Output_HI"

REM --- Verify the fixed Python script exists ---
if not exist "%PYFIX%" (
  echo [ERROR] Fixed script not found: "%PYFIX%"
  echo Place make_audiobook_hi_FIXED.py in this folder and try again.
  pause
  exit /b 1
)

REM Optional: remove the old buggy file so nothing calls it by accident
if exist "%BASE%make_audiobook_hi.py" del /q "%BASE%make_audiobook_hi.py"

REM --- Activate venv and ensure dependencies ---
if exist "%VENV%" (
  call "%VENV%"
) else (
  echo [WARN] Could not find venv at "%VENV%". Continuing with system Python...
)
if exist "%REQ%" (
  echo [INFO] Installing requirements from "%REQ%"
  pip install -r "%REQ%"
)

REM --- Ensure output folder exists ---
if not exist "%OUTPUT%" mkdir "%OUTPUT%"

REM --- Process PDFs (Unicode-safe enumeration via PowerShell) ---
for /f "usebackq delims=" %%F in (`
  powershell -NoProfile -Command ^
    "Get-ChildItem -LiteralPath '%INPUT%' -Filter *.pdf | %%{$_.FullName}"
`) do (
  echo [RUN] Processing %%F
  python "%PYFIX%" --pdf "%%F" --out "%OUTPUT%" --voice hi-IN-SwaraNeural --zip_chunk 3 --skip_existing
  if errorlevel 1 (
    echo [WARN] Python returned a non-zero exit code for: %%F
  )
)

echo.
echo Done. Check "%OUTPUT%".
echo (Tip) ffmpeg is optional; only needed if you want enforced 192k re-encode.
pause
