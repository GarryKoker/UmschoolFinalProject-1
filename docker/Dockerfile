FROM python:3.11-slim

WORKDIR /app

# Скопировать только requirements сначала для кэширования слоёв
COPY requirements.txt .

# Установить системные зависимости для сборки и netcat-openbsd для проверки порта
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev netcat-openbsd && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*

# Копируем весь проект
COPY . .

# По умолчанию ждать доступности БД и запускать бота
CMD ["bash", "-c", "until nc -z db ${POSTGRES_PORT:-5432}; do echo 'waiting for db'; sleep 1; done; python main.py"]