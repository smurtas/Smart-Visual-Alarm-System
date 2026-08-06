"""
Receive JPEG alert images from the ESP32-S3-EYE.

The most recent image is stored as:
runtime/images/latest.jpg
"""

from pathlib import Path
import os
import tempfile

from flask import Flask, jsonify, request


PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIRECTORY = PROJECT_ROOT / "runtime" / "images"
LATEST_IMAGE = IMAGE_DIRECTORY / "latest.jpg"

MAX_IMAGE_SIZE = 2 * 1024 * 1024

app = Flask(__name__)


@app.post("/upload-alert")
def upload_alert():
    """Receive one raw JPEG image in the HTTP request body."""

    if request.content_type != "image/jpeg":
        return jsonify(
            {
                "status": "error",
                "message": "Content-Type must be image/jpeg",
            }
        ), 415

    image_data = request.get_data(cache=False)

    if not image_data:
        return jsonify(
            {
                "status": "error",
                "message": "Empty request body",
            }
        ), 400

    if len(image_data) > MAX_IMAGE_SIZE:
        return jsonify(
            {
                "status": "error",
                "message": "Image too large",
            }
        ), 413

    # Basic JPEG signature validation.
    if not (
        image_data.startswith(b"\xff\xd8")
        and image_data.endswith(b"\xff\xd9")
    ):
        return jsonify(
            {
                "status": "error",
                "message": "Invalid JPEG data",
            }
        ), 400

    IMAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    # Atomic replacement prevents Node-RED from reading a partial file.
    file_descriptor, temporary_path = tempfile.mkstemp(
        prefix="latest-",
        suffix=".jpg",
        dir=IMAGE_DIRECTORY,
    )

    try:
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            temporary_file.write(image_data)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, LATEST_IMAGE)

    except Exception:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise

    return jsonify(
        {
            "status": "ok",
            "bytes": len(image_data),
            "path": str(LATEST_IMAGE),
        }
    ), 201


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "latest_image_exists": LATEST_IMAGE.exists(),
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )