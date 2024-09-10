# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=app.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project into the container
COPY . /app

# Apply database migrations
# RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Create superuser (optional, якщо потрібно)
# RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email=os.environ.get('DJANGO_SUPERUSER_EMAIL')).exists() or User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_EMAIL'), 'admin', os.environ.get('DJANGO_SUPERUSER_PASSWORD'))" | python manage.py shell

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]

# Expose the port
EXPOSE 8000
