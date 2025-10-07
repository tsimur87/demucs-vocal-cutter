@echo off
setlocal enabledelayedexpansion

:: Переход в корневую директорию проекта
cd /d "%~dp0\.."
if errorlevel 1 (
    echo Не удалось перейти в директорию проекта.
    exit /b 1
)

echo Запуск Demucs Vocal Cutter...

:: Определение директории виртуальной среды
set VENV_DIR=venv
set PYTHON=%VENV_DIR%\Scripts\python.exe

:: Проверка наличия виртуальной среды
echo Проверка виртуальной среды...
if not exist "%VENV_DIR%" (
    echo Создание виртуальной среды...
    python -m venv "%VENV_DIR%"
)

:: Проверка, что Python в виртуальной среде существует
if not exist "%PYTHON%" (
    echo Виртуальная среда не найдена или повреждена. Пожалуйста, пересоздайте её.
    exit /b 1
)

echo Используется Python: %PYTHON%

:: Активация виртуальной среды
call "%VENV_DIR%\Scripts\activate.bat"

:: Обновление pip
echo Обновление pip...
pip install --upgrade pip

:: Установка зависимостей
echo Установка зависимостей из requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Не удалось установить некоторые зависимости. Пробуем установить основные...
    pip install demucs ffmpeg-python yt-dlp pytube tqdm scipy
)

:: Установка PyTorch
echo Установка PyTorch...
pip install torch==2.7.1 torchaudio==2.7.1 torchvision==0.22.1

:: Проверка наличия ffmpeg
echo Проверка ffmpeg...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo FFmpeg не найден. Установите его и добавьте в PATH.
    exit /b 1
)

:: Обработка аргументов
set URL=
set MODEL=
:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--url" (
    set URL=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--model" (
    set MODEL=%~2
    shift
    shift
    goto parse_args
)
echo Неизвестный параметр: %1
exit /b 1
:end_parse

:: Проверка доступных моделей
set VALID_MODELS=htdemucs htdemucs_ft htdemucs_6s hdemucs_mmi mdx mdx_extra mdx_q mdx_extra_q
set MODEL_VALID=0
if not defined MODEL set MODEL_VALID=0
for %%m in (%VALID_MODELS%) do (
    if /i "%MODEL%"=="%%m" set MODEL_VALID=1
)
if %MODEL_VALID%==0 (
    echo Доступные модели Demucs:
    echo 1. htdemucs (быстрее, стандартное качество, 4 стема)
    echo 2. htdemucs_ft (медленнее, лучшее качество, 4 стема)
    echo 3. htdemucs_6s (стандартная скорость, 6 стемов, хорошее для гитары)
    echo 4. hdemucs_mmi (баланс скорости и качества, 4 стема)
    echo 5. mdx (высокое качество, стандартная скорость, 4 стема)
    echo 6. mdx_extra (лучшее качество, стандартная скорость, 4 стема)
    echo 7. mdx_q (быстрее, ниже качество, 4 стема)
    echo 8. mdx_extra_q (быстрее, ниже качество, 4 стема)
    set /p MODEL_CHOICE="Выберите модель (1-8, Enter для htdemucs): "
    if "!MODEL_CHOICE!"=="2" set MODEL=htdemucs_ft
    if "!MODEL_CHOICE!"=="3" set MODEL=htdemucs_6s
    if "!MODEL_CHOICE!"=="4" set MODEL=hdemucs_mmi
    if "!MODEL_CHOICE!"=="5" set MODEL=mdx
    if "!MODEL_CHOICE!"=="6" set MODEL=mdx_extra
    if "!MODEL_CHOICE!"=="7" set MODEL=mdx_q
    if "!MODEL_CHOICE!"=="8" set MODEL=mdx_extra_q
    if "!MODEL_CHOICE!"=="" set MODEL=htdemucs
    if not "!MODEL!"=="htdemucs" if not "!MODEL!"=="htdemucs_ft" if not "!MODEL!"=="htdemucs_6s" if not "!MODEL!"=="hdemucs_mmi" if not "!MODEL!"=="mdx" if not "!MODEL!"=="mdx_extra" if not "!MODEL!"=="mdx_q" if not "!MODEL!"=="mdx_extra_q" set MODEL=htdemucs
)

:: Запуск основного скрипта
echo Запуск Demucs Vocal Cutter с моделью: %MODEL%
if defined URL (
    "%PYTHON%" -m demucs_vocal_cutter.main --url "%URL%" --model "%MODEL%"
) else (
    "%PYTHON%" -m demucs_vocal_cutter.main --model "%MODEL%"
)
endlocal