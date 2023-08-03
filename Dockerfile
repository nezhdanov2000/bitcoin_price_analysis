# Используем образ Python как базовый образ
FROM python:3

# Создание директории приложения внутри контейнера
WORKDIR /app

# Копирование файлов .py в директорию приложения в контейнере
COPY main.py /app/main.py
COPY config.py /app/config.py
COPY request.py /app/request.py
COPY analysis.py /app/analysis.py

# Устанавливаем переменные окружения
ENV POSTGRES_HOST = localhost 
ENV POSTGRES_PORT = 5432 
ENV POSTGRES_DB = postgres 
ENV POSTGRES_USER = postgres 
ENV POSTGRES_PASSWORD = mega55555 

# Файл сценария Python в контейнер
COPY main.py /app

# Устанавливаем библиотеку
RUN pip install requests psycopg2-binary

# CMD для main.py и ввода пользователя
CMD ["python", "main.py"]
