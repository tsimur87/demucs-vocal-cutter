import os
import logging
import threading
import yt_dlp
from .utils import get_platform_config

def detect_platform(url):
    """Определение платформы по URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url:
        return 'instagram'
    return 'unknown'

def get_video_title(url, platform):
    """Получение заголовка видео"""
    try:
        ydl_opts = get_platform_config(platform)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.prepare_filename(info).rsplit('.', 1)[0]
    except Exception as e:
        logging.error(f"Ошибка получения заголовка: {str(e)}")
        return "output"

def get_available_video_qualities(url, platform):
    """Получение доступных качеств видео"""
    try:
        ydl_opts = get_platform_config(platform)
        ydl_opts['quiet'] = True
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            qualities = []
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('ext') == 'mp4':
                    quality = {
                        'id': f.get('format_id'),
                        'resolution': f.get('resolution', 'Unknown'),
                        'description': f.get('format_note', ''),
                    }
                    qualities.append(quality)
            return qualities
    except Exception as e:
        logging.error(f"Ошибка получения качеств видео: {str(e)}")
        return [{'id': 'best', 'resolution': 'Unknown', 'description': 'Default'}]

def download_audio(url, temp_dir, platform):
    """Загрузка аудио"""
    try:
        ydl_opts = get_platform_config(platform)
        ydl_opts.update({
            'outtmpl': os.path.join(temp_dir, 'audio_orig.%(ext)s'),
            'format': 'bestaudio[ext=m4a]',
        })
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        logging.error(f"Ошибка загрузки аудио: {str(e)}")
        return None

def start_video_download(url, output_path, quality_id, platform):
    """Запуск загрузки видео в отдельном потоке"""
    def download():
        try:
            ydl_opts = get_platform_config(platform)
            ydl_opts.update({
                'outtmpl': output_path,
                'format': quality_id,
                'merge_output_format': 'mp4',
            })
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logging.error(f"Ошибка загрузки видео: {str(e)}")

    thread = threading.Thread(target=download)
    thread.start()
    return thread