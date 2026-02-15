# Скрипт для компиляции APK через Docker на Windows (PowerShell)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Nexus Ultra Dark - Android APK Builder" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Проверка Docker
try {
    docker --version | Out-Null
} catch {
    Write-Host "ERROR: Docker не установлен!" -ForegroundColor Red
    Write-Host "Установите Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

try {
    docker ps | Out-Null
} catch {
    Write-Host "ERROR: Docker не запущен!" -ForegroundColor Red
    Write-Host "Запустите Docker Desktop и попробуйте снова." -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
Write-Host "✓ Docker готов" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Создание Docker образа..." -ForegroundColor Yellow
docker build -t nexus-apk-builder .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Ошибка при создании образа" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
Write-Host "✓ Образ создан" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] Запуск компиляции..." -ForegroundColor Yellow
$current_dir = (Get-Location).Path
docker run -v "${current_dir}:/workspace" nexus-apk-builder buildozer android debug

Write-Host ""
Write-Host "[4/4] Проверка результата..." -ForegroundColor Yellow
$apk_files = Get-ChildItem -Path "./bin" -Filter "*.apk" -ErrorAction SilentlyContinue

if ($apk_files) {
    Write-Host ""
    Write-Host "✓ SUCCESS! APK готов в папке bin\" -ForegroundColor Green
    Write-Host ""
    foreach ($file in $apk_files) {
        Write-Host "  📦 $($file.Name)" -ForegroundColor Cyan
        Write-Host "  📏 Размер: $([math]::Round($file.Length / 1MB, 2)) MB" -ForegroundColor Gray
    }
} else {
    Write-Host "ERROR: APK файл не найден" -ForegroundColor Red
}

Write-Host ""
Read-Host "Нажмите Enter для выхода"

