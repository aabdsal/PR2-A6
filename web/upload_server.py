from __future__ import annotations

from pathlib import Path
import uuid
from PIL import Image
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os
STATIC_DIR = Path(__file__).parent
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "web" / "uploads"

def _allowed_file(file) -> bool:
    try:
        file.seek(0)
        img = Image.open(file)
        es_png = img.format == "PNG"
        file.seek(0)
        return es_png
    except:
        return False

@app.after_request
def _add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Servir archivos estáticos (index.html, script.js, style.css, images, etc.)
@app.route("/")
def serve_index():
    return send_file(STATIC_DIR / "index.html")

# Servir imágenes y otros archivos estáticos
@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(STATIC_DIR / "images", filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/uploads", methods=["POST", "OPTIONS"])
def upload_png():
    if request.method == "OPTIONS":
        return ("", 204)

    if "file" not in request.files:
        return jsonify({"error": "Falta el archivo"}), 400

    file = request.files["file"]

    if not file or file.filename == "":
        return jsonify({"error": "Archivo vacío"}), 400

    if not _allowed_file(file.stream):
        return jsonify({"error": "El archivo no es un PNG válido"}), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(f"label_{uuid.uuid4().hex}.png")
    save_path = UPLOAD_DIR / filename
    file.save(save_path)

    return jsonify({
        "ruta_relativa": f"uploads/{filename}"
    })


def start_server(host: str = "0.0.0.0", port: int = 5001):
    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    start_server()