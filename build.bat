@echo off
setlocal

echo Installing build dependencies...
python -m pip install --upgrade pip
pip install pyinstaller customtkinter psutil requests "qrcode[pil]" Pillow tzdata cryptography

echo Running syntax check...
python -m py_compile toolbox.py toolbox_api.py polybuild.py

echo Building Toolbox.exe...
if exist "icon.ico" (
    pyinstaller --noconfirm --clean --noconsole --onefile --name Toolbox ^
        --add-data "plugins;plugins" ^
        --add-data "polybuild.py;." ^
        --hidden-import "toolbox_api" ^
        --hidden-import "PIL._tkinter_finder" ^
        --hidden-import "zoneinfo" ^
        --hidden-import "cryptography.fernet" ^
        --collect-all "customtkinter" ^
        --collect-data "tzdata" ^
        --collect-submodules "qrcode" ^
        --icon "icon.ico" ^
        "toolbox.py"
) else (
    pyinstaller --noconfirm --clean --noconsole --onefile --name Toolbox ^
        --add-data "plugins;plugins" ^
        --add-data "polybuild.py;." ^
        --hidden-import "toolbox_api" ^
        --hidden-import "PIL._tkinter_finder" ^
        --hidden-import "zoneinfo" ^
        --hidden-import "cryptography.fernet" ^
        --collect-all "customtkinter" ^
        --collect-data "tzdata" ^
        --collect-submodules "qrcode" ^
        "toolbox.py"
)

if errorlevel 1 (
    echo PyInstaller build failed.
    exit /b %errorlevel%
)

if not exist "dist\Toolbox.exe" (
    echo ERROR: dist\Toolbox.exe not found
    exit /b 1
)

echo Build complete: dist\Toolbox.exe
dir /b "dist\Toolbox.exe"
