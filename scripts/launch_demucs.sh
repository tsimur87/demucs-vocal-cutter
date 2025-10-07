#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")/.."

echo "Starting Demucs Vocal Cutter..."

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH."
    echo "Please install Python3 and try again."
    read -p "Press Enter to close this window..."
    exit 1
fi

# Remove existing virtual environment if it's corrupted
if [ -d "venv" ]; then
    echo "Checking virtual environment..."
    if [ ! -f "venv/bin/python3" ] && [ ! -f "venv/bin/python" ]; then
        echo "Virtual environment appears corrupted. Removing and recreating..."
        rm -rf venv
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        echo "Please make sure Python3 and venv module are properly installed."
        read -p "Press Enter to close this window..."
        exit 1
    fi
fi

# Determine the correct Python executable path
if [ -f "venv/bin/python3" ]; then
    PYTHON_EXEC="venv/bin/python3"
    PIP_EXEC="venv/bin/pip3"
elif [ -f "venv/bin/python" ]; then
    PYTHON_EXEC="venv/bin/python"
    PIP_EXEC="venv/bin/pip"
else
    echo "Error: Could not find Python executable in virtual environment."
    read -p "Press Enter to close this window..."
    exit 1
fi

echo "Using Python: $PYTHON_EXEC"

# Upgrade pip
echo "Upgrading pip..."
$PYTHON_EXEC -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
$PIP_EXEC install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install some dependencies. Trying core dependencies..."
    $PIP_EXEC install demucs ffmpeg-python yt-dlp pytube tqdm scipy
    # Try PyTorch separately
    echo "Installing PyTorch..."
    $PIP_EXEC install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1
fi

# Check for ffmpeg
echo "Checking for ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: ffmpeg not found in system PATH."
    echo "You may need to install ffmpeg: https://ffmpeg.org/download.html"
fi

# Run the script
echo "Launching Demucs Vocal Cutter..."
echo "================================================"
$PYTHON_EXEC -m demucs_vocal_cutter.main
echo "================================================"
echo "Process completed."
read -p "Press Enter to close this window..."