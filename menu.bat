@echo off
REM Открытие основных файлов инструкций
cls

echo.
echo ===============================================
echo Nexus Ultra Dark - APK Builder
echo ===============================================
echo.
echo Выберите что открыть:
echo.
echo 1. START_HERE.txt - НАЧНИТЕ ОТСЮДА!
echo 2. BUILD_APK_FULL_GUIDE.txt - Полная инструкция
echo 3. ANDROID_COMPILE_GUIDE.txt - Варианты сборки
echo 4. build_apk.ps1 - СКРИПТ СБОРКИ (запуск)
echo 5. Открыть папку в Explorer
echo 6. Выход
echo.

set /p choice="Выберите (1-6): "

if "%choice%"=="1" (
    start notepad START_HERE.txt
) else if "%choice%"=="2" (
    start notepad BUILD_APK_FULL_GUIDE.txt
) else if "%choice%"=="3" (
    start notepad ANDROID_COMPILE_GUIDE.txt
) else if "%choice%"=="4" (
    powershell -ExecutionPolicy Bypass -File build_apk.ps1
) else if "%choice%"=="5" (
    explorer .
) else if "%choice%"=="6" (
    exit /b 0
) else (
    echo Неверный выбор!
)

pause

