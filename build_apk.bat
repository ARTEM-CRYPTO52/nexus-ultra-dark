@echo off
REM Скрипт для компиляции APK через Docker на Windows

echo ===============================================
echo Nexus Ultra Dark - Android APK Builder
echo ===============================================
echo.

REM Проверка Docker
docker --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker не установлен!
    echo Установите Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/4] Проверка Docker...
docker ps > nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker не запущен!
    echo Запустите Docker Desktop и попробуйте снова.
    pause
    exit /b 1
)
echo ✓ Docker готов

echo.
echo [2/4] Создание Docker образа...
docker build -t nexus-apk-builder .
if errorlevel 1 (
    echo ERROR: Ошибка при создании образа
    pause
    exit /b 1
)
echo ✓ Образ создан

echo.
echo [3/4] Запуск компиляции...
REM Получаем полный путь текущей папки
for /f "delims=" %%i in ('cd') do set "current_dir=%%i"

docker run -v "%current_dir%:/workspace" nexus-apk-builder buildozer android debug
if errorlevel 1 (
    echo ERROR: Ошибка при компиляции
    pause
    exit /b 1
)

echo.
echo [4/4] Проверка результата...
if exist "bin\*.apk" (
    echo.
    echo ✓ SUCCESS! APK готов в папке bin\
    echo.
    dir /b bin\*.apk
) else (
    echo ERROR: APK файл не найден
)

pause

