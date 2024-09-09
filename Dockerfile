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
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project into the container
COPY . /app

# Apply database migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]

# Expose the port
EXPOSE 8000
