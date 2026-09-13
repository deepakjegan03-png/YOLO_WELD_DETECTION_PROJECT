import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# YOLO Model Configuration
# Path to the trained YOLO weights file
MODEL_PATH = os.environ.get("YOLO_MODEL_PATH", os.path.join(BASE_DIR, "models", "best.pt"))

# Fallback path in case models/best.pt is missing but runs/ exists
FALLBACK_MODEL_PATH = os.path.join(
    BASE_DIR, "runs", "detect", "weld_detection_project", "weld_yolo_training", "weights", "best.pt"
)

# Inference settings
DEFAULT_CONFIDENCE_THRESHOLD = 0.25
MIN_CONFIDENCE_THRESHOLD = 0.10
MAX_CONFIDENCE_THRESHOLD = 0.95
IMAGE_SIZE = 640

# File Upload Settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "static", "results")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Megabytes maximum upload size

# Server Settings
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
DEBUG = False
