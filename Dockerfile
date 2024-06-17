# Используем официальный образ Python в качестве базового образа
FROM python:3.11.4

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в рабочую директорию
COPY . /app

# Устанавливаем зависимости
RUN pip install gunicorn

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN python manage.py collectstatic --noinput

# Открываем порт для приложения
EXPOSE $PORT

# Запускаем сервер Django
CMD ["sh", "-c", "gunicorn news_portal.wsgi:application --bind 0.0.0.0:$PORT"]

