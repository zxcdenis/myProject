# Используем официальный образ Python в качестве базового образа
FROM python:3.11.4

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в рабочую директорию
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт для приложения
EXPOSE 8000

# Запускаем сервер Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 news_portal.wsgi:application"]
