@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ====== All-PDFs Audiobook Launcher (Neat) ======
REM Drop PDFs into "Input". Outputs in "Output\<PDF name>\" as MP3s.

set "ROOT=%~dp0"
pushd "%ROOT%"
set "INPUT=%ROOT%Input"
set "OUTPUT=%ROOT%Output"

if not exist "%INPUT%" mkdir "%INPUT%"
if not exist "%OUTPUT%" mkdir "%OUTPUT%"

where py >nul 2>nul && (set "PY=py") || (set "PY=python")

REM Settings
set "VOICE=en-US-JennyNeural"
set "BITRATE=192k"
set "PAUSE=600"
set "ZIPCHUNK=3"

REM Ensure our script exists
if not exist "%ROOT%make_audiobook.py" (
  echo [ERROR] make_audiobook.py not found in "%ROOT%"
  pause
  exit /b 1
)

echo [STEP] Installing dependencies...
%PY% -m pip install -r "%ROOT%requirements.txt"

REM Warn if ffmpeg not on PATH (we still run; WAVs may remain if offline fallback kicks in)
where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo [WARN] FFmpeg not found on PATH. Install it for clean MP3 output: winget install Gyan.FFmpeg
)

set "COUNT=0"
for %%F in ("%INPUT%\*.pdf") do (
  set "PDF=%%~fF"
  set "NAME=%%~nF"
  set "SAFE=!NAME: =_!"
  set "OUTDIR=%OUTPUT%\!SAFE!"

  if not exist "!OUTDIR!" mkdir "!OUTDIR!"

  echo.
  echo [RUN] !NAME!
  %PY% "%ROOT%make_audiobook.py" --pdf "!PDF!" --out "!OUTDIR!" --voice "%VOICE%" --bitrate "%BITRATE%" --pause_ms %PAUSE% --zip_chunk %ZIPCHUNK% --skip_existing

  if errorlevel 1 (
    echo [WARN] Failed: !NAME!
  ) else (
    echo [OK] Done: !NAME!
  )
  set /a COUNT+=1
)

if "!COUNT!"=="0" (
  echo [INFO] No PDFs found in Input.
) else (
  echo.
  echo [DONE] Processed !COUNT! file^(s^). Check the Output folder.
)
echo.
pause
popd
endlocal
