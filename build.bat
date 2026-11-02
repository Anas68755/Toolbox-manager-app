@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Ultimate Toolbox Pro - Build

echo ============================================
echo   Ultimate Toolbox Pro - Windows EXE build
echo ============================================
echo.

REM ---- 1. Find Python (py launcher first, then python) ----
set "PY="
REM Prefer a Python that has prebuilt llama-cpp-python wheels (3.12, 3.11, 3.10)
for %%V in (3.12 3.11 3.10) do if not defined PY py -%%V --version >nul 2>&1 && set "PY=py -%%V"
if not defined PY where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
    echo [X] Python 3 was not found. Install it from https://www.python.org/downloads/
    echo     and tick "Add python.exe to PATH" during setup.
    goto :fail
)
echo [i] Using: %PY%
%PY% --version
echo.

REM ---- 2. Virtual environment (keeps your system Python clean) ----
if not exist ".venv\Scripts\python.exe" (
    echo [1/5] Creating virtual environment .venv ...
    %PY% -m venv .venv
    if errorlevel 1 goto :fail
) else (
    echo [1/5] Using existing virtual environment .venv
)
set "VPY=.venv\Scripts\python.exe"

REM ---- 3. Dependencies ----
echo [2/5] Installing dependencies ...
"%VPY%" -m pip install --upgrade pip >nul
"%VPY%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto :fail

REM ---- Optional: llama-cpp-python (in-process LLM inside the EXE) ----
REM Prebuilt CPU wheels exist for Python 3.12 and older. If none is available
REM the EXE is still built; it then uses the llama.cpp *server* backend.
set "LLAMA="
echo [i] Trying to add llama-cpp-python (optional, prebuilt wheel only) ...
"%VPY%" -m pip install llama-cpp-python --only-binary=:all: --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu >nul 2>&1
"%VPY%" -c "import llama_cpp" >nul 2>&1
if not errorlevel 1 (
    set "LLAMA=--collect-all llama_cpp"
    echo [OK] llama-cpp-python will be bundled into the EXE.
) else (
    echo [i] llama-cpp-python not available for this Python - the EXE will use the
    echo     llama.cpp server backend instead ^(Backend = "llama.cpp Server ^(auto-start^)"^).
    echo     Tip: if you just installed Python 3.12, delete the .venv folder and run this again.
)

REM ---- 4. Syntax check ----
echo [3/5] Checking syntax ...
"%VPY%" -m py_compile toolbox.py toolbox_api.py polybuild.py
if errorlevel 1 goto :fail

REM ---- 5. Build (same options as .github/workflows/build.yaml) ----
echo [4/5] Building Toolbox.exe (this takes a few minutes) ...
set "ICON="
if exist "icon.ico" set "ICON=--icon icon.ico"

"%VPY%" -m PyInstaller --noconfirm --clean --noconsole --onefile ^
  --name Toolbox ^
  --add-data "plugins;plugins" ^
  --add-data "polybuild.py;." ^
  --hidden-import toolbox_api ^
  --hidden-import PIL._tkinter_finder ^
  --hidden-import zoneinfo ^
  --hidden-import cryptography.fernet ^
  --collect-all customtkinter ^
  --collect-data tzdata ^
  --collect-submodules qrcode ^
  %LLAMA% %ICON% toolbox.py
if errorlevel 1 goto :fail

REM ---- 6. Verify ----
echo [5/5] Verifying output ...
if not exist "dist\Toolbox.exe" (
    echo [X] dist\Toolbox.exe was not created.
    goto :fail
)

echo.
echo ============================================
echo   SUCCESS:  dist\Toolbox.exe
echo ============================================
echo Your settings, notes and vaults are stored next to the EXE.
echo.
pause
exit /b 0

:fail
echo.
echo [X] Build failed. Scroll up to see the first error message.
echo.
pause
exit /b 1
