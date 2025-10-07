import os
import logging
import yt_dlp

def get_platform_config(platform):
    """Возвращает конфигурацию для yt-dlp в зависимости от платформы"""
    base_config = {
        'quiet': False,
        'noprogress': False,
        'format_sort': ['+res', '+vcodec:h264'],
        'noplaylist': True,
        'continuedl': True,
    }
    if platform == 'youtube':
        return {**base_config, 'cookiefile': None}
    elif platform == 'tiktok':
        return {**base_config, 'extractor_args': {'tiktok': {'app_version': '28.2.2'}}}
    elif platform == 'instagram':
        return {**base_config, 'cookiefile': None}
    return base_config

def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    dependencies = ['yt_dlp', 'ffmpeg', 'torch', 'torchaudio', 'scipy']
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    return missing

def clean_directory(temp_dir, model_name, files_to_remove):
    """Очистка временной директории, кроме папки модели"""
    try:
        model_dir = os.path.join(temp_dir, model_name)
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if item_path == model_dir or item_path in files_to_remove:
                continue
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
    except Exception as e:
        logging.error(f"Ошибка очистки директории: {str(e)}")