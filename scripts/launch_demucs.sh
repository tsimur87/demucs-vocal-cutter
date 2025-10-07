#!/bin/bash

# Переход в корневую директорию проекта
cd "$(dirname "$0")/.."

echo "Запуск Demucs Vocal Cutter..."

# Определение директории виртуальной среды
VENV_DIR="./venv"
PYTHON="$VENV_DIR/bin/python3"

# Проверка наличия виртуальной среды
if [ ! -d "$VENV_DIR" ]; then
    echo "Создание виртуальной среды..."
    python3 -m venv "$VENV_DIR"
fi

# Проверка, что Python в виртуальной среде существует
echo "Проверка виртуальной среды..."
if [ ! -f "$PYTHON" ]; then
    echo "Виртуальная среда не найдена или повреждена. Пожалуйста, пересоздайте её."
    exit 1
fi

echo "Используется Python: $PYTHON"

# Активация виртуальной среды
source "$VENV_DIR/bin/activate"

# Обновление pip
echo "Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
echo "Установка зависимостей из requirements.txt..."
if ! pip install -r requirements.txt; then
    echo "Не удалось установить некоторые зависимости. Пробуем установить основные..."
    pip install demucs ffmpeg-python yt-dlp pytube tqdm scipy
fi

# Установка PyTorch, если не установлен
echo "Установка PyTorch..."
pip install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1

# Проверка наличия ffmpeg
echo "Проверка ffmpeg..."
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "FFmpeg не найден. Установите его с помощью 'brew install ffmpeg'."
    exit 1
fi

# Обработка аргументов
URL=""
MODEL="htdemucs"  # Модель по умолчанию
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --url) URL="$2"; shift ;;
        --model) MODEL="$2"; shift ;;
        *) echo "Неизвестный параметр: $1"; exit 1 ;;
    esac
    shift
done

# Проверка доступных моделей
VALID_MODELS=("htdemucs" "htdemucs_ft" "htdemucs_6s")
if [[ ! " ${VALID_MODELS[@]} " =~ " ${MODEL} " ]]; then
    echo "Доступные модели Demucs:"
    echo "1. htdemucs (быстрее, стандартное качество)"
    echo "2. htdemucs_ft (медленнее, лучшее качество)"
    echo "3. htdemucs_6s (6 источников, высокое качество, медленнее)"
    read -p "Выберите модель (1-3, по умолчанию 1): " MODEL_CHOICE
    case $MODEL_CHOICE in
        2) MODEL="htdemucs_ft" ;;
        3) MODEL="htdemucs_6s" ;;
        *) MODEL="htdemucs" ;;
    esac
fi

# Запуск основного скрипта
echo "Запуск Demucs Vocal Cutter с моделью: $MODEL"
if [ -n "$URL" ]; then
    "$PYTHON" -m demucs_vocal_cutter.main --url "$URL" --model "$MODEL"
else
    "$PYTHON" -m demucs_vocal_cutter.main --model "$MODEL"
fi