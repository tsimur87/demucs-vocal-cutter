import os
import subprocess
import logging
import ffmpeg
from tqdm import tqdm
import demucs.separate
import torch

try:
    from scipy.io import wavfile
    scipy_available = True
except ImportError:
    scipy_available = False

def convert_audio_to_wav(input_path, output_path):
    """Конвертация аудио в WAV для обработки Demucs"""
    try:
        ffmpeg.input(input_path).output(output_path, **{"ar": 44100}).run(overwrite_output=True)
        return os.path.isfile(output_path)
    except Exception as e:
        logging.error(f"Не удалось конвертировать аудио в WAV: {str(e)}")
        try:
            cmd = ["ffmpeg", "-i", input_path, "-ar", "44100", "-ac", "2", output_path, "-y"]
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
            return os.path.isfile(output_path)
        except Exception as e:
            logging.error(f"Ошибка FFmpeg subprocess: {str(e)}")
            return False

def run_demucs(audio_file, temp_dir, model_name):
    """Запуск разделения Demucs с использованием MPS или CPU"""
    try:
        # Установка устройства (MPS для Apple Silicon, CUDA для NVIDIA, иначе CPU)
        device = "cpu"
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            device = "mps"
            logging.info("Используется MPS (Apple Silicon GPU)")
        elif torch.cuda.is_available():
            device = "cuda"
            logging.info("Используется CUDA (NVIDIA GPU)")
        else:
            logging.info("MPS/CUDA недоступны, используется CPU")

        # Убедимся, что директория существует
        os.makedirs(temp_dir, exist_ok=True)
        output_dir = os.path.join(temp_dir, model_name)
        os.makedirs(output_dir, exist_ok=True)

        # Запуск Demucs с указанным устройством
        demucs.separate.main([
            "--float32",
            "--two-stems", "vocals",
            "-n", model_name,
            "-o", temp_dir,
            "--device", device,
            audio_file
        ])

        # Путь к файлу вокала
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        vocals_path = os.path.join(temp_dir, model_name, base_name, "vocals.wav")
        if os.path.exists(vocals_path):
            logging.info(f"Файл вокала создан: {vocals_path}")
            return vocals_path
        else:
            logging.error(f"Файл вокала не найден: {vocals_path}")
            return None
    except Exception as e:
        logging.error(f"Ошибка разделения Demucs: {str(e)}")
        return None

def merge_audio_and_video(video_file, audio_file, output_file):
    """Объединение видео и аудио с помощью FFmpeg"""
    try:
        video_in = ffmpeg.input(video_file)
        audio_in = ffmpeg.input(audio_file)
        out = ffmpeg.output(video_in.video, audio_in.audio, output_file, vcodec="copy", acodec="aac", strict="experimental")
        out.run(overwrite_output=True)
        return True
    except Exception as e:
        logging.error(f"Не удалось объединить аудио и видео: {str(e)}")
        try:
            cmd = ["ffmpeg", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_file, "-y"]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logging.error(f"Ошибка FFmpeg merge subprocess: {str(e)}")
            return False