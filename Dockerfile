# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости  --no-cache-dir
RUN pip install -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

#CMD ["python", "app.py", "runserver"]