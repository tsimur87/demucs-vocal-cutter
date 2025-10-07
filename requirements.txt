# Основные компоненты для разделения звука
demucs==4.0.1
# PyTorch: версия зависит от платформы
# Для macOS (Apple Silicon): torch==2.7.1, torchaudio==2.7.1, torchvision==0.22.1
# Для Windows/Linux (CPU): pip install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
# Для Windows/Linux (GPU): pip install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu121
torch==2.7.1
torchaudio==2.7.1
torchvision==0.22.1

# Инструменты для скачивания медиа
yt-dlp==2025.6.9
pytube==15.0.0

# Обработка аудио и видео
ffmpeg-python==0.2.0
lameenc==1.8.1
openunmix==1.3.0
scipy==1.15.3

# Основные зависимости и утилиты
numpy==2.3.0
omegaconf==2.3.0
tqdm==4.67.1
PyYAML==6.0.2
pillow==11.2.1

# Второстепенные зависимости
antlr4-python3-runtime==4.9.3
cloudpickle==3.1.1
dora_search==0.1.12
einops==0.8.1
filelock==3.18.0
fsspec==2025.5.1
future==1.0.0
Jinja2==3.1.6
julius==0.2.7
MarkupSafe==3.0.2
mpmath==1.3.0
networkx==3.5
retrying==1.3.4
setuptools==80.9.0
six==1.17.0
submitit==1.5.3
sympy==1.14.0
treetable==0.2.5
typing_extensions==4.14.0