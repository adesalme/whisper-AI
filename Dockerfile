# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    WHISPER_MODEL=large-v3

WORKDIR /app

# Système: ffmpeg requis par Whisper
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# Installer torch CPU explicitement depuis l'index CPU de PyTorch puis les deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.3.1+cpu \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app /app/app

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-k", "gthread", "-t", "0", "-b", "0.0.0.0:8000", "app.main:app"]


