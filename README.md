сюда добавь # Demucs Vocal Cutter

Extract vocals from videos or audio files from various platforms (YouTube, TikTok, etc.) using Demucs.

---

**Demucs Vocal Cutter** — это инструмент для **очищения видео от музыки**, который извлекает только вокал из видеофайлов или аудио с YouTube, TikTok, Instagram или локальных файлов. Проект использует библиотеку **Demucs** для разделения аудиодорожки на вокал и инструментал, удаляя музыку (барабаны, бас, гитары и другие инструменты), чтобы оставить чистый вокал. Видео загружается в **лучшем доступном качестве MP4**, а обработка оптимизирована для скорости с использованием MPS (на macOS) или CPU/GPU (на Windows). Пользователь может выбрать одну из 8 моделей Demucs, где htdemucs используется по умолчанию при нажатии Enter для быстрого и качественного очищения.

**Основные возможности**:

* **Очищение от музыки**: Удаляет весь инструментал, оставляя только вокал с помощью --two-stems vocals.
* **Автоматический выбор качества**: Видео загружается в лучшем формате MP4 (bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]).
* **Гибкость моделей**: Поддержка 8 моделей Demucs для разного баланса качества и скорости (htdemucs по умолчанию).
* **Автоматизация**: Активация виртуальной среды, установка зависимостей, проверка FFmpeg.
* **Кроссплатформенность**: Работает на Windows (launch\_demucs.bat) и macOS (launch\_demucs.sh).
* **Интеграция с WebStorm**: Полная поддержка запуска и отладки.

**Применение**: Идеально для создания акапелла-версий видео, удаления фоновой музыки для подкастов, караоке или анализа вокала. Поддерживает видео с YouTube, TikTok, Instagram или локальные файлы в форматах MP4, AVI, MOV, MKV, MP3, WAV.

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
