# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=5001

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic-dev \
    libmagic1 \
    libpq-dev \
    postgresql-client \
    tesseract-ocr \
    tesseract-ocr-tur \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data/uploads

# Set Tesseract data path
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
