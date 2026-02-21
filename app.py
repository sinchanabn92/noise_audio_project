from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import uuid
from utils import process_chunk

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


# =========================
# 🎤 LIVE 5-SECOND CHUNK
# =========================
@app.route("/process_chunk", methods=["POST"])
def process_audio_chunk():

    if "audio" not in request.files:
        return jsonify({"error": "No audio received"})

    # Get selected language (default English)
    language = request.form.get("language", "en")

    file = request.files["audio"]

    unique_id = str(uuid.uuid4())
    audio_path = os.path.join(UPLOAD_FOLDER, unique_id + ".webm")
    file.save(audio_path)

    text, tts_filename = process_chunk(audio_path, language)

    return jsonify({
        "text": text,
        "audio": tts_filename
    })


# =========================
# 📁 FILE UPLOAD
# =========================
@app.route("/upload", methods=["POST"])
def upload_audio():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    # Get selected language
    language = request.form.get("language", "en")

    file = request.files["file"]

    unique_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    audio_path = os.path.join(UPLOAD_FOLDER, unique_id + "." + ext)
    file.save(audio_path)

    text, tts_filename = process_chunk(audio_path, language)

    return jsonify({
        "text": text,
        "audio": tts_filename
    })


# =========================
# 🔊 SERVE CLEAN AUDIO
# =========================
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)