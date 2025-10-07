@echo off
cd /d "%~dp0\.."

echo Starting Demucs Vocal Cutter...

:: Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python3 and try again.
    pause
    exit /b 1
)

:: Remove existing virtual environment if it's corrupted
if exist venv (
    echo Checking virtual environment...
    if not exist venv\Scripts\python.exe (
        echo Virtual environment appears corrupted. Removing and recreating...
        rmdir /s /q venv
    )
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        echo Please make sure Python3 and venv module are properly installed.
        pause
        exit /b 1
    )
)

:: Set Python and pip executables
set PYTHON_EXEC=venv\Scripts\python.exe
set PIP_EXEC=venv\Scripts\pip.exe

echo Using Python: %PYTHON_EXEC%

:: Upgrade pip
echo Upgrading pip...
%PYTHON_EXEC% -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies from requirements.txt...
%PIP_EXEC% install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Failed to install some dependencies. Trying core dependencies...
    %PIP_EXEC% install demucs ffmpeg-python yt-dlp pytube tqdm scipy
    echo Installing PyTorch...
    %PIP_EXEC% install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
)

:: Check for ffmpeg
echo Checking for ffmpeg...
where ffmpeg >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Warning: ffmpeg not found in system PATH.
    echo You may need to install ffmpeg: https://ffmpeg.org/download.html
    echo.
)

:: Run the script
echo Launching Demucs Vocal Cutter...
echo ================================================
%PYTHON_EXEC% -m demucs_vocal_cutter.main
echo ================================================
echo Process completed.
pause