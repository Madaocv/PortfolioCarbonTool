# Використовуємо базовий образ Python
FROM python:3.10-slim

# Встановлюємо змінні оточення
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=app.settings

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Python залежності
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо проект
COPY . /app

# Застосовуємо міграції
RUN python manage.py migrate

# Збираємо статичні файли
RUN python manage.py collectstatic --noinput

# Create superuser
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email=os.environ.get('DJANGO_SUPERUSER_EMAIL')).exists() or User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_EMAIL'), 'admin', os.environ.get('DJANGO_SUPERUSER_PASSWORD'))" | python manage.py shell

# Копіюємо конфігураційний файл для Nginx у правильне місце
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Запускаємо Nginx та Gunicorn разом
CMD service nginx start && gunicorn --bind 0.0.0.0:8000 app.wsgi:application

# Відкриваємо порти
EXPOSE 8000
