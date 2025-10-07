import os
import subprocess
import re
import threading
import shutil
import logging

try:
    from pytube import YouTube
    pytube_available = True
except ImportError:
    pytube_available = False

from demucs_vocal_cutter import config

SUPPORTED_PLATFORMS = config['supported_platforms']

def detect_platform(url):
    """Detect which platform the URL is from"""
    for platform, domains in SUPPORTED_PLATFORMS.items():
        if any(domain in url.lower() for domain in domains):
            return platform
    return "unknown"

def get_available_video_qualities(url, platform="youtube"):
    """Get available video qualities for the given URL"""
    try:
        if platform == "youtube":
            try:
                subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                cmd = ["yt-dlp", "-F", url]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                formats = []
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('['):
                        if "format code" in line.lower() or "---" in line:
                            continue
                        parts = line.split()
                        if len(parts) >= 2 and not line.startswith('['):
                            format_id = parts[0]
                            if format_id.lower() in ['format', 'id', '---'] or not format_id.replace('-', '').replace('_', '').isalnum():
                                continue
                            if 'audio only' in line.lower():
                                continue
                            resolution = "unknown"
                            for part in parts:
                                if 'x' in part and any(c.isdigit() for c in part):
                                    resolution = part
                                    break
                            formats.append({
                                'id': format_id,
                                'resolution': resolution,
                                'description': line.strip()
                            })
                return formats
            except Exception:
                if pytube_available:
                    try:
                        yt = YouTube(url)
                        formats = []
                        for stream in yt.streams.filter(progressive=True).order_by('resolution'):
                            formats.append({
                                'id': stream.itag,
                                'resolution': stream.resolution,
                                'description': f"{stream.resolution}, {stream.mime_type}, {stream.fps}fps"
                            })
                        return formats
                    except Exception:
                        pass
        return [
            {'id': 'best', 'resolution': 'best', 'description': 'Best quality'},
            {'id': '720p', 'resolution': '720p', 'description': 'HD (720p)'},
            {'id': '480p', 'resolution': '480p', 'description': 'SD (480p)'},
            {'id': '360p', 'resolution': '360p', 'description': 'Low (360p)'}
        ]
    except Exception as e:
        logging.error(f"Failed to get video qualities: {str(e)}")
        return [{'id': 'best', 'resolution': 'best', 'description': 'Best quality'}]

def download_audio(video_url, temp_dir, platform="youtube"):
    """Download just the audio from various platforms using yt-dlp"""
    try:
        subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        audio_temp_path = os.path.join(temp_dir, "audio_orig.m4a")
        audio_cmd = ["yt-dlp", "--format", "bestaudio[ext=m4a]/bestaudio", "--output", audio_temp_path, "--no-playlist", video_url]
        subprocess.run(audio_cmd, check=True)
        if os.path.exists(audio_temp_path):
            return audio_temp_path
        return None
    except Exception as e:
        logging.error(f"Failed to download audio from {platform}: {str(e)}")
        if pytube_available and platform == "youtube":
            try:
                yt = YouTube(video_url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_temp_path = os.path.join(temp_dir, "audio_orig.m4a")
                audio_stream.download(output_path=temp_dir, filename="audio_orig.m4a")
                return audio_temp_path
            except Exception as e:
                logging.error(f"Pytube fallback failed: {str(e)}")
        return None

def start_video_download(video_url, video_file, quality_id='best', platform="youtube"):
    """Start downloading the video in a background thread with selected quality"""
    def download_video_ytdlp():
        try:
            # Use 'b' instead of 'best' to let yt-dlp choose the best available format
            format_option = quality_id if quality_id != 'best' else 'b'
            cmd = ["yt-dlp", "--format", format_option, "--output", video_file, "--no-playlist", video_url]
            subprocess.run(cmd, check=True)
        except Exception as e:
            logging.error(f"Failed to download video from {platform}: {str(e)}")
    video_thread = threading.Thread(target=download_video_ytdlp)
    video_thread.start()
    return video_thread

def get_video_title(url, platform="youtube"):
    """Get the title of the video from the URL"""
    try:
        cmd = ["yt-dlp", "--get-title", url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        title = result.stdout.strip()
        if title:
            title = re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
            return title
    except Exception as e:
        logging.error(f"Failed to get video title with yt-dlp: {str(e)}")
        if pytube_available and platform == "youtube":
            try:
                yt = YouTube(url)
                title = yt.title
                return re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
            except Exception as e:
                logging.error(f"Pytube title fetch failed: {str(e)}")
    return "output_vocals"