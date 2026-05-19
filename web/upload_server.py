"""Servidor sencillo para subir PNGs desde la web."""

from __future__ import annotations

from pathlib import Path
import uuid

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "web" / "uploads"
ALLOWED_EXTENSIONS = {".png"}


def _allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.after_request
def _add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_png():
    if request.method == "OPTIONS":
        return ("", 204)

    if "file" not in request.files:
        return jsonify({"error": "Falta el archivo"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Archivo vacio"}), 400

    filename = file.filename
    if not filename:
        return jsonify({"error": "Archivo vacio"}), 400
    
    if not _allowed_file(filename):
        return jsonify({"error": "Solo se permiten PNG"}), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(f"label_{uuid.uuid4().hex}.png")
    save_path = UPLOAD_DIR / filename
    file.save(save_path)

    return jsonify({"ruta_relativa": f"uploads/{filename}"})


def start_server(host: str = "0.0.0.0", port: int = 5001):
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    start_server()
