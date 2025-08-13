import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


def get_device() -> str:
    try:
        import torch  # type: ignore

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


APP_TITLE = "Whisper Transcriber (large-v3)"
MODEL_NAME = os.getenv("WHISPER_MODEL", "large-v3")
DEVICE = os.getenv("WHISPER_DEVICE", get_device())

app = Flask(__name__, template_folder=str(Path(__file__).parent / "templates"))
CORS(app)


whisper_model = None


def ensure_model_loaded() -> None:
    global whisper_model
    if whisper_model is None:
        import whisper  # type: ignore

        whisper_model = whisper.load_model(MODEL_NAME, device=DEVICE)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title=APP_TITLE,
        model=MODEL_NAME,
        device=DEVICE,
    )


@app.route("/transcribe", methods=["POST"])
def transcribe():
    ensure_model_loaded()

    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400

    file = request.files["file"]
    language: Optional[str] = request.form.get("language") or None

    if not file.filename.lower().endswith((".mp3", ".wav", ".m4a", ".mp4", ".mpeg", ".mpga", ".webm", ".ogg")):
        return jsonify({"error": "Format non supporté. Veuillez envoyer un fichier audio (mp3/wav/m4a/...)"}), 400

    tmp_dir = Path(tempfile.mkdtemp(prefix="whisper_"))
    tmp_audio = tmp_dir / file.filename

    try:
        with tmp_audio.open("wb") as buffer:
            shutil.copyfileobj(file.stream, buffer)

        options = {
            "task": "transcribe",
            "fp16": DEVICE == "cuda",
        }
        if language:
            options["language"] = language

        result = whisper_model.transcribe(str(tmp_audio), **options)  # type: ignore[name-defined]

        return jsonify(
            {
                "text": result.get("text", "").strip(),
                "language": result.get("language", language),
                "segments": result.get("segments", []),
                "model": MODEL_NAME,
                "device": DEVICE,
            }
        )
    finally:
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception:
            pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)


