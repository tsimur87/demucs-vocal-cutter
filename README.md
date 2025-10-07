# Demucs Vocal Cutter

Extract vocals from videos or audio files from various platforms (YouTube, TikTok, etc.) using Demucs.

## Features

- Supports multiple platforms: YouTube, TikTok, Instagram, etc.
- Separates vocals using Demucs models (`htdemucs`, `htdemucs_ft`).
- Allows quality selection for video downloads.
- Processes local files or URLs.
- Cross-platform: Windows, macOS, Linux.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/demucs-vocal-cutter.git
   cd demucs-vocal-cutter
   ```


2. Install FFmpeg: [FFmpeg download](https://ffmpeg.org/download.html)
3. Run the appropriate script:
   * **macOS/Linux**: ./scripts/launch\_demucs.sh
   * **Windows**: scripts\\launch\_demucs.bat

## Usage

Run interactively:

bash

```
python -m demucs_vocal_cutter.main
```

Or with arguments:

bash

```
python -m demucs_vocal_cutter.main --url <video_url> --model htdemucs_ft --quality best
```

## Requirements

* Python 3.8+
* FFmpeg
* See requirements.txt for Python dependencies

## License

MIT
