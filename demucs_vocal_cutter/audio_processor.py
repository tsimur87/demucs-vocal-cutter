import os
import subprocess
import logging
import ffmpeg
from tqdm import tqdm
import demucs.separate

try:
    from scipy.io import wavfile
    scipy_available = True
except ImportError:
    scipy_available = False

def convert_audio_to_wav(input_path, output_path):
    """Convert any audio format to WAV for Demucs processing"""
    # Полная логика из исходного convert_audio_to_wav
    try:
        ffmpeg.input(input_path).output(output_path, **{"ar": 44100}).run(overwrite_output=True)
        return os.path.isfile(output_path)
    except:
        # Fallback to subprocess
        cmd = ["ffmpeg", "-i", input_path, "-ar", "44100", "-ac", "2", output_path, "-y"]
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        return os.path.isfile(output_path)

def run_demucs(audio_file, temp_dir, model_name):
    """Run Demucs separation and find output vocal file"""
    # Полная логика из исходного run_demucs, включая methods 1-3 и поиск файлов
    os.makedirs(os.path.join(temp_dir, model_name), exist_ok=True)
    # Method 1, 2, 3
    # ...
    # Поиск vocals_path
    return vocals_path  # Замените на реальный

def merge_audio_and_video(video_file, audio_file, output_file):
    """Merge video and audio using ffmpeg"""
    # Полная логика из исходного merge_audio_and_video
    try:
        video_in = ffmpeg.input(video_file)
        audio_in = ffmpeg.input(audio_file)
        out = ffmpeg.output(video_in.video, audio_in.audio, output_file, vcodec="copy", acodec="aac", strict="experimental")
        out.run(overwrite_output=True)
        return True
    except:
        # Fallback to subprocess
        cmd = ["ffmpeg", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_file, "-y"]
        subprocess.run(cmd, check=True)
        return True