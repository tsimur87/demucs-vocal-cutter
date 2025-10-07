import os
import subprocess
import logging
import shutil

logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s")

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    # Логика из исходного check_dependencies для ffmpeg, yt-dlp, pytube, demucs
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except:
        missing_deps.append("ffmpeg")
    # ... остальные проверки
    return missing_deps

def clean_directory(temp_dir, model_name=None, files_to_remove=None):
    """Clean up temporary files"""
    # Полная логика из исходного clean_directory
    if files_to_remove:
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)
    if model_name and os.path.isdir(os.path.join(temp_dir, model_name)):
        shutil.rmtree(os.path.join(temp_dir, model_name))
    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
        os.rmdir(temp_dir)