# Используем базовый образ с Java и Python
FROM ubuntu:22.04

# Установка переменных окружения
ENV ANDROID_HOME=/root/android-sdk \
    ANDROID_SDK_ROOT=/root/android-sdk \
    PATH=$PATH:/root/android-sdk/cmdline-tools/latest/bin:/root/android-sdk/platform-tools

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    openjdk-11-jdk \
    git \
    ant \
    wget \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка BuildTools и SDK
RUN mkdir -p /root/android-sdk/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip commandlinetools-linux-9477386_latest.zip -d /root/android-sdk/cmdline-tools && \
    rm commandlinetools-linux-9477386_latest.zip && \
    mv /root/android-sdk/cmdline-tools/cmdline-tools /root/android-sdk/cmdline-tools/latest

# Установка Android SDK
RUN yes | sdkmanager "platforms;android-31" "build-tools;31.0.0" "ndk;25.2.9519653"

# Установка Python пакетов
RUN pip3 install --upgrade pip setuptools && \
    pip3 install buildozer cython kivy requests python-for-android

# Рабочая папка
WORKDIR /workspace

# Команда компиляции
CMD ["buildozer", "android", "debug"]

