import os
import sys
import logging
import threading
import argparse
from demucs_vocal_cutter import config
from demucs_vocal_cutter.downloader import detect_platform, get_available_video_qualities, download_audio, start_video_download, get_video_title
from demucs_vocal_cutter.audio_processor import convert_audio_to_wav, run_demucs, merge_audio_and_video
from demucs_vocal_cutter.utils import check_dependencies, clean_directory

stop_event = threading.Event()

def parse_args():
    parser = argparse.ArgumentParser(description="Извлечение вокала из видео/аудио")
    parser.add_argument("--url", help="URL видео")
    parser.add_argument("--file", help="Путь к локальному файлу")
    parser.add_argument("--model", default="htdemucs", choices=["htdemucs", "htdemucs_ft", "htdemucs_6s"], help="Модель Demucs (htdemucs: быстрее, htdemucs_ft: лучшее качество, htdemucs_6s: 6 источников)")
    parser.add_argument("--quality", default=None, help="Качество видео")
    return parser.parse_args()

def main():
    args = parse_args()

    print("""
    ╔════════════════════════════════════════════════╗
    ║  Enhanced Demucs Vocal Cutter                  ║
    ║  Извлечение вокала из видео с YouTube, TikTok,║
    ║  Instagram с выбором качества                  ║
    ╚════════════════════════════════════════════════╝
    """)

    missing = check_dependencies()
    if missing:
        print("Предупреждение: Отсутствуют зависимости:", ", ".join(missing))
        if input("Продолжить? (y/n): ").strip().lower() != 'y':
            sys.exit("Выход из-за отсутствия зависимостей.")

    video_path = args.url or args.file or input("Введите URL или 'local' для файла из папки Inputs: ").strip()
    platform = "local" if not video_path.startswith("http") else detect_platform(video_path)
    print(f"Обнаружена платформа: {platform}")

    model_name = args.model
    quality_id = args.quality or config['default_quality']

    temp_dir = config['temp_dir']
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(config['output_dir'], exist_ok=True)

    audio_file = os.path.join(temp_dir, "audio_input.wav")
    video_file = os.path.join(temp_dir, "video_input.mp4")

    if video_path.startswith("http"):
        video_title = get_video_title(video_path, platform)
        output_filename = f"{video_title}_vocals.mp4"
    else:
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_filename = f"{base_name}_vocals.mp4"
    output_file = os.path.join(config['output_dir'], output_filename)

    downloaded_video = False
    video_thread = None
    audio_orig_path = None

    try:
        if video_path.lower() == 'local':
            input_dir = config['input_dir']
            os.makedirs(input_dir, exist_ok=True)
            input_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav'))]
            if not input_files:
                sys.exit("Файлы в папке Inputs не найдены.")
            print("\nДоступные файлы:")
            for i, file in enumerate(input_files):
                print(f"{i+1}. {file}")
            choice = int(input("Выберите номер файла: ")) - 1
            video_path = os.path.join(input_dir, input_files[choice])

        if video_path.startswith("http"):
            available_qualities = get_available_video_qualities(video_path, platform)
            print("\nДоступные качества видео:")
            for i, quality in enumerate(available_qualities):
                print(f"{i+1}. {quality.get('resolution', 'Unknown')} - {quality.get('description', '')}")
            try:
                quality_choice = int(input("\nВыберите качество (номер): ")) - 1
                quality_id = available_qualities[quality_choice]['id']
            except (ValueError, IndexError):
                print("Неверный выбор, используется качество по умолчанию (лучшее).")
                quality_id = 'best'

            audio_orig_path = download_audio(video_path, temp_dir, platform)
            if not audio_orig_path:
                sys.exit("Не удалось загрузить аудио.")
            if not convert_audio_to_wav(audio_orig_path, audio_file):
                sys.exit("Не удалось конвертировать аудио в WAV.")
            video_thread = start_video_download(video_path, video_file, quality_id, platform)
            downloaded_video = True
        else:
            if not convert_audio_to_wav(video_path, audio_file):
                sys.exit("Не удалось конвертировать аудио в WAV.")
            shutil.copy2(video_path, video_file)
            downloaded_video = True

        vocals_path = run_demucs(audio_file, temp_dir, model_name)
        if not vocals_path:
            sys.exit("Не удалось разделить вокал. Проверьте логи.")

        if video_thread and video_thread.is_alive():
            print("Ожидание загрузки видео...")
            video_thread.join()

        if stop_event.is_set():
            sys.exit("Процесс прерван.")

        if not os.path.exists(video_file):
            sys.exit("Видеофайл не найден. Загрузка могла не удаться.")

        if not merge_audio_and_video(video_file, vocals_path, output_file):
            sys.exit("Не удалось объединить аудио и видео.")

        print(f"Успех! Результат: {output_file}")

    except KeyboardInterrupt:
        stop_event.set()
        if video_thread:
            video_thread.join(timeout=5)
        sys.exit(1)
    except Exception as e:
        logging.exception(str(e))
        print(f"Ошибка: {str(e)}")
        sys.exit(1)
    finally:
        files_to_remove = [audio_file]
        if audio_orig_path:
            files_to_remove.append(audio_orig_path)
        if downloaded_video:
            files_to_remove.append(video_file)
        clean_directory(temp_dir, model_name, files_to_remove)

if __name__ == "__main__":
    main()