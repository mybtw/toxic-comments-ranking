# Используйте официальный образ NVIDIA CUDA с Python
FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

# Установка рабочей директории в контейнере
WORKDIR /app

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов приложения в контейнер
COPY app /app

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["./start.sh"]
