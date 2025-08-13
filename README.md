## Configuration CUDA

Ce projet est configuré pour utiliser CUDA pour accélérer la transcription audio avec Whisper.

### Prérequis CUDA

1. **GPU NVIDIA** avec support CUDA
2. **Drivers NVIDIA** installés
3. **Docker avec support NVIDIA** (pour l'exécution en conteneur)

### Vérifier la configuration CUDA

```bash
python check_cuda.py
```

## Lancer en local (sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.main:app
export WHISPER_DEVICE=cuda  # Utiliser CUDA
flask run --host 0.0.0.0 --port 8000
```

## Lancer avec Docker

1. Construire l'image

```bash
docker build -t whisper-ai-web:latest .
```

2. Démarrer le conteneur avec CUDA

```bash
# Avec Docker (nécessite nvidia-docker)
docker run --rm --gpus all -p 8000:8000 -e WHISPER_MODEL=large-v3 -e WHISPER_DEVICE=cuda whisper-ai-web:latest

# Ou via docker-compose (recommandé)
docker compose up --build
```

Ensuite ouvrez `http://localhost:8000`.

# whisper-AI
