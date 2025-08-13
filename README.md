## Lancer en local (sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.main:app
flask run --host 0.0.0.0 --port 8000
```

## Lancer avec Docker

1. Construire l'image

```bash
docker build -t whisper-ai-web:latest .
```

2. Démarrer le conteneur

```bash
docker run --rm -p 8000:8000 -e WHISPER_MODEL=large-v3 -e WHISPER_DEVICE=cpu whisper-ai-web:latest
```

Ou via docker-compose:

```bash
docker compose up --build
```

Ensuite ouvrez `http://localhost:8000`.
# whisper-AI
