import os
import re
import uuid
import time
import base64
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import numpy as np

import config
from utils.detector import YOLODetector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

# Ensure required directories exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.RESULTS_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)

# Global detector instance (loaded once at startup)
detector = None
model_error_message = None

def init_detector():
    """Initializes the YOLODetector instance once at startup."""
    global detector, model_error_message
    model_file = config.MODEL_PATH

    # Check fallback if default path doesn't exist
    if not os.path.exists(model_file) and hasattr(config, "FALLBACK_MODEL_PATH") and os.path.exists(config.FALLBACK_MODEL_PATH):
        logger.info(f"Default model not found at {model_file}. Using fallback: {config.FALLBACK_MODEL_PATH}")
        model_file = config.FALLBACK_MODEL_PATH

    try:
        detector = YOLODetector(
            model_path=model_file,
            default_conf=config.DEFAULT_CONFIDENCE_THRESHOLD,
            img_size=config.IMAGE_SIZE
        )
        logger.info("YOLO detector initialized successfully.")
    except Exception as e:
        model_error_message = str(e)
        logger.error(f"Failed to initialize YOLO detector: {e}")

# Initialize detector
init_detector()


def is_allowed_file(filename):
    """Validates file extension against allowed image extensions."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def parse_confidence(conf_val):
    """Safely parses and bounds confidence threshold value."""
    try:
        if conf_val is None or str(conf_val).strip() == "":
            return config.DEFAULT_CONFIDENCE_THRESHOLD
        c = float(conf_val)
        return float(np.clip(c, config.MIN_CONFIDENCE_THRESHOLD, config.MAX_CONFIDENCE_THRESHOLD))
    except (ValueError, TypeError):
        return config.DEFAULT_CONFIDENCE_THRESHOLD


@app.errorhandler(413)
def file_too_large(e):
    """Handle upload exceeding MAX_CONTENT_LENGTH."""
    max_mb = config.MAX_CONTENT_LENGTH // (1024 * 1024)
    return jsonify({
        "success": False,
        "error": f"Uploaded file is too large. Maximum allowed size is {max_mb}MB."
    }), 413


@app.route("/", methods=["GET"])
def index():
    """Renders the main dashboard page."""
    model_loaded = detector is not None
    classes = list(detector.class_names.values()) if model_loaded else []
    return render_template(
        "index.html",
        model_loaded=model_loaded,
        model_error=model_error_message,
        classes=classes,
        default_conf=config.DEFAULT_CONFIDENCE_THRESHOLD
    )


@app.route("/health", methods=["GET"])
def health():
    """Health and status endpoint."""
    return jsonify({
        "status": "running",
        "model_loaded": detector is not None,
        "model_path": detector.model_path if detector else config.MODEL_PATH,
        "classes": list(detector.class_names.values()) if detector else [],
        "error": model_error_message
    })


@app.route("/uploads/<path:filename>", methods=["GET"])
def serve_upload(filename):
    """Serves uploaded source images."""
    return send_from_directory(config.UPLOAD_FOLDER, filename)


@app.route("/detect", methods=["POST"])
def detect():
    """Handles image upload and runs YOLO object detection."""
    global detector
    if detector is None:
        return jsonify({
            "success": False,
            "error": "YOLO model is not loaded. Please ensure 'models/best.pt' is present on the server."
        }), 500

    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided in the request."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No image file selected."}), 400

    if not is_allowed_file(file.filename):
        allowed = ", ".join(sorted(list(config.ALLOWED_EXTENSIONS)))
        return jsonify({
            "success": False,
            "error": f"Invalid file type '{file.filename}'. Allowed formats: {allowed}."
        }), 400

    try:
        # Generate unique filenames to prevent caching and collisions
        timestamp = int(time.time() * 1000)
        unique_id = uuid.uuid4().hex[:8]
        safe_orig_name = secure_filename(file.filename)
        ext = safe_orig_name.rsplit(".", 1)[1].lower() if "." in safe_orig_name else "jpg"
        
        orig_filename = f"upload_{timestamp}_{unique_id}.{ext}"
        result_filename = f"result_{timestamp}_{unique_id}.jpg"
        
        orig_filepath = os.path.join(config.UPLOAD_FOLDER, orig_filename)
        result_filepath = os.path.join(config.RESULTS_FOLDER, result_filename)

        # Save uploaded file
        file.save(orig_filepath)

        # Read image with OpenCV
        image = cv2.imread(orig_filepath)
        if image is None:
            return jsonify({
                "success": False,
                "error": "Failed to decode image. File may be corrupted or in an unsupported format."
            }), 400

        # Parse confidence threshold
        conf_threshold = parse_confidence(request.form.get("confidence"))

        # Run inference
        annotated_image, detections = detector.detect(image, conf_threshold=conf_threshold)

        # Save annotated result image
        cv2.imwrite(result_filepath, annotated_image)

        return jsonify({
            "success": True,
            "original_image": f"/uploads/{orig_filename}",
            "result_image": f"/static/results/{result_filename}",
            "total_detections": len(detections),
            "confidence_used": conf_threshold,
            "detections": detections
        })

    except Exception as e:
        logger.error(f"Error during /detect inference: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"An error occurred while processing the image: {str(e)}"
        }), 500


@app.route("/detect_webcam", methods=["POST"])
def detect_webcam():
    """Handles captured webcam frames transmitted as Base64 images."""
    global detector
    if detector is None:
        return jsonify({
            "success": False,
            "error": "YOLO model is not loaded. Please ensure 'models/best.pt' is present on the server."
        }), 500

    data = request.get_json(silent=True)
    if not data or "image" not in data:
        return jsonify({"success": False, "error": "No image data provided in webcam request."}), 400

    base64_data = data["image"]
    if not isinstance(base64_data, str) or not base64_data.strip():
        return jsonify({"success": False, "error": "Empty or invalid webcam image data."}), 400

    try:
        # Strip Data URL header if present (e.g. data:image/jpeg;base64,...)
        if "," in base64_data:
            base64_data = base64_data.split(",", 1)[1]

        # Decode base64 bytes
        img_bytes = base64.b64decode(base64_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({
                "success": False,
                "error": "Failed to decode webcam frame into a valid image."
            }), 400

        # Generate unique filenames
        timestamp = int(time.time() * 1000)
        unique_id = uuid.uuid4().hex[:8]
        orig_filename = f"webcam_orig_{timestamp}_{unique_id}.jpg"
        result_filename = f"webcam_result_{timestamp}_{unique_id}.jpg"

        orig_filepath = os.path.join(config.UPLOAD_FOLDER, orig_filename)
        result_filepath = os.path.join(config.RESULTS_FOLDER, result_filename)

        # Save original frame
        cv2.imwrite(orig_filepath, image)

        # Parse confidence threshold
        conf_threshold = parse_confidence(data.get("confidence"))

        # Run inference
        annotated_image, detections = detector.detect(image, conf_threshold=conf_threshold)

        # Save annotated result image
        cv2.imwrite(result_filepath, annotated_image)

        return jsonify({
            "success": True,
            "original_image": f"/uploads/{orig_filename}",
            "result_image": f"/static/results/{result_filename}",
            "total_detections": len(detections),
            "confidence_used": conf_threshold,
            "detections": detections
        })

    except Exception as e:
        logger.error(f"Error during /detect_webcam inference: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"An error occurred while processing the webcam frame: {str(e)}"
        }), 500


@app.route("/clear", methods=["POST"])
def clear_results():
    """Cleans up temporary uploaded and detection result files."""
    deleted_count = 0
    folders = [config.UPLOAD_FOLDER, config.RESULTS_FOLDER]
    now = time.time()

    for folder in folders:
        if os.path.exists(folder):
            for fname in os.listdir(folder):
                fpath = os.path.join(folder, fname)
                try:
                    if os.path.isfile(fpath):
                        # Delete files older than 60 seconds or all on explicit request
                        os.remove(fpath)
                        deleted_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove temporary file {fpath}: {e}")

    return jsonify({
        "success": True,
        "message": f"Temporary cache cleared ({deleted_count} files removed)."
    })


def print_banner():
    """Prints beginner-friendly startup banner displaying local server URL."""
    banner = f"""
============================================================
              YOLO OBJECT DETECTION SERVER
============================================================
 Model Path : {config.MODEL_PATH}
 Status     : {'READY' if detector is not None else 'MODEL MISSING'}
 Local URL  : http://{config.SERVER_HOST}:{config.SERVER_PORT}
============================================================
 Open http://{config.SERVER_HOST}:{config.SERVER_PORT} in your web browser.
 Press CTRL+C to stop the server.
============================================================
"""
    print(banner)


if __name__ == "__main__":
    print_banner()
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.DEBUG
    )
