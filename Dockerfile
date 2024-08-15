# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN pip install flask

# Копируем наш скрипт в контейнер
COPY main.py /main.py

# Указываем рабочую директорию
WORKDIR /

# Открываем порт 8080
EXPOSE 8080

# Команда для запуска приложения
CMD ["python", "main.py"]
