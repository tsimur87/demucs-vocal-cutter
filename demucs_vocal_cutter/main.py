import os
import sys
import logging
import threading
import argparse
import yaml
from demucs_vocal_cutter.downloader import detect_platform, get_available_video_qualities, download_audio, start_video_download, get_video_title
from demucs_vocal_cutter.audio_processor import convert_audio_to_wav, run_demucs, merge_audio_and_video
from demucs_vocal_cutter.utils import check_dependencies, clean_directory

stop_event = threading.Event()

def load_config(config_path="demucs_vocal_cutter/config.yaml"):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def parse_args():
    parser = argparse.ArgumentParser(description="Extract vocals from video/audio")
    parser.add_argument("--url", help="URL of the video")
    parser.add_argument("--file", help="Path to local file")
    parser.add_argument("--model", default=None, help="Demucs model (htdemucs or htdemucs_ft)")
    parser.add_argument("--quality", default=None, help="Video quality")
    return parser.parse_args()

def main():
    config = load_config()
    args = parse_args()

    print("""
    ╔════════════════════════════════════════════════╗
    ║  Enhanced Demucs Vocal Cutter                  ║
    ║  Extract vocals from videos on multiple        ║
    ║  platforms including YouTube, TikTok, and      ║
    ║  Instagram with quality selection              ║
    ╚════════════════════════════════════════════════╝
    """)

    missing = check_dependencies()
    if missing:
        print("Warning: Missing dependencies:", ", ".join(missing))
        if input("Proceed anyway? (y/n): ").strip().lower() != 'y':
            sys.exit("Exiting due to missing dependencies.")

    video_path = args.url or args.file or input("Enter URL or 'local' for file from Inputs folder: ").strip()
    platform = "local" if not video_path.startswith("http") else detect_platform(video_path)
    print(f"Detected platform: {platform}")

    model_name = args.model or config['default_model']
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
                sys.exit("No files found in Inputs folder.")
            print("\nAvailable files:")
            for i, file in enumerate(input_files):
                print(f"{i+1}. {file}")
            choice = int(input("Select file number: ")) - 1
            video_path = os.path.join(input_dir, input_files[choice])

        if video_path.startswith("http"):
            available_qualities = get_available_video_qualities(video_path, platform)
            print("\nAvailable video qualities:")
            for i, quality in enumerate(available_qualities):
                print(f"{i+1}. {quality.get('resolution', 'Unknown')} - {quality.get('description', '')}")
            try:
                quality_choice = int(input("\nSelect quality (number): "))
                quality_id = available_qualities[quality_choice - 1]['id']
            except:
                print("Using default quality.")
            audio_orig_path = download_audio(video_path, temp_dir, platform)
            if not audio_orig_path:
                sys.exit("Failed to download audio.")
            convert_audio_to_wav(audio_orig_path, audio_file)
            video_thread = start_video_download(video_path, video_file, quality_id, platform)
            downloaded_video = True
        else:
            convert_audio_to_wav(video_path, audio_file)
            shutil.copy2(video_path, video_file)
            downloaded_video = True

        vocals_path = run_demucs(audio_file, temp_dir, model_name)
        if not vocals_path:
            sys.exit("Failed to separate vocals.")

        if video_thread and video_thread.is_alive():
            print("Waiting for video download...")
            video_thread.join()

        if stop_event.is_set():
            sys.exit("Process interrupted.")

        if not os.path.exists(video_file):
            sys.exit("Video file not found.")

        merge_audio_and_video(video_file, vocals_path, output_file)
        print(f"Success! Output: {output_file}")

    except KeyboardInterrupt:
        stop_event.set()
        if video_thread:
            video_thread.join(timeout=5)
        sys.exit(1)
    except Exception as e:
        logging.exception(str(e))
        print(f"Error: {str(e)}")
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