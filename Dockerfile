# syntax=docker/dockerfile:1

FROM nvidia/cuda:12.1-devel-ubuntu22.04 AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    WHISPER_MODEL=large-v3

WORKDIR /app

# Système: Python, ffmpeg et dépendances CUDA
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-dev \
        python3-pip \
        ffmpeg \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3.12 /usr/bin/python

COPY requirements.txt /app/requirements.txt

# Installer PyTorch avec CUDA et les dépendances
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app /app/app

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-k", "gthread", "-t", "0", "-b", "0.0.0.0:8000", "app.main:app"]


