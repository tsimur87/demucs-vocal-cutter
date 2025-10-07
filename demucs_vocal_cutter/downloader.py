# demucs_vocal_cutter/downloader.py
import os
import subprocess
from pytube import YouTube
import re

def detect_platform(url):
    SUPPORTED_PLATFORMS = {
        "youtube": ["youtube.com", "youtu.be"],
        "tiktok": ["tiktok.com"],
        # ... остальные платформы
    }
    for platform, domains in SUPPORTED_PLATFORMS.items():
        if any(domain in url.lower() for domain in domains):
            return platform
    return "unknown"

def download_audio(video_url, temp_dir, platform="youtube"):
    # Код функции download_audio из исходного файла
    pass

# Другие функции: get_available_video_qualities, start_video_download, get_video_title