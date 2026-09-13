import os
import io
import base64
import glob
import pytest
from app import app
import config
from utils.detector import YOLODetector

def test_health_endpoint():
    """Verify /health endpoint returns running status and model info."""
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "running"
    assert data["model_loaded"] is True
    assert len(data["classes"]) > 0
    print("\n[PASS] Health check passed:", data)

def test_index_page():
    """Verify home page loads HTML with 200 status."""
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"YOLO Object Detection" in res.data
    assert b"Upload Image" in res.data
    assert b"Webcam Detection" in res.data
    print("\n[PASS] Index page rendered successfully.")

def test_detect_image_upload():
    """Verify /detect endpoint processes uploaded images properly."""
    client = app.test_client()
    test_images = glob.glob("datasets/test/images/*.jpg")
    assert len(test_images) > 0, "No test images found in datasets/test/images/"

    test_img_path = test_images[0]
    with open(test_img_path, "rb") as f:
        img_bytes = f.read()

    data = {
        "image": (io.BytesIO(img_bytes), "test_sample.jpg"),
        "confidence": "0.25"
    }

    res = client.post("/detect", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "result_image" in res_data
    assert "detections" in res_data
    assert isinstance(res_data["detections"], list)

    # Verify result image file exists on disk
    rel_path = res_data["result_image"].lstrip("/")
    abs_path = os.path.join(config.BASE_DIR, rel_path)
    assert os.path.exists(abs_path), f"Result image {abs_path} does not exist on disk"

    print(f"\n[PASS] Image upload detection passed: {len(res_data['detections'])} detections.")
    if res_data["detections"]:
        det = res_data["detections"][0]
        assert "bbox" in det
        assert "class_name" in det
        assert "confidence" in det
        print("Sample detection:", det)

def test_detect_invalid_file_extension():
    """Verify /detect rejects non-image files with friendly error message."""
    client = app.test_client()
    data = {
        "image": (io.BytesIO(b"fake text content"), "malicious_script.txt"),
        "confidence": "0.25"
    }
    res = client.post("/detect", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    res_data = res.get_json()
    assert res_data["success"] is False
    assert "Invalid file type" in res_data["error"]
    print("\n[PASS] Invalid file rejection passed:", res_data["error"])

def test_detect_missing_image_payload():
    """Verify /detect rejects empty payload with 400."""
    client = app.test_client()
    res = client.post("/detect", data={}, content_type="multipart/form-data")
    assert res.status_code == 400
    res_data = res.get_json()
    assert res_data["success"] is False
    print("\n[PASS] Empty payload rejection passed.")

def test_detect_webcam_base64():
    """Verify /detect_webcam handles Base64 images."""
    client = app.test_client()
    test_images = glob.glob("datasets/test/images/*.jpg")
    assert len(test_images) > 0

    with open(test_images[0], "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image": f"data:image/jpeg;base64,{encoded}",
        "confidence": 0.20
    }

    res = client.post("/detect_webcam", json=payload)
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    assert "result_image" in res_data
    assert "detections" in res_data
    print(f"\n[PASS] Webcam Base64 detection passed: {res_data['total_detections']} detections.")

def test_clear_endpoint():
    """Verify /clear endpoint cleans temporary files."""
    client = app.test_client()
    res = client.post("/clear")
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data["success"] is True
    print("\n[PASS] Clear endpoint passed:", res_data["message"])

def test_missing_model_exception():
    """Verify YOLODetector raises FileNotFoundError with helpful advice if model path is invalid."""
    try:
        YOLODetector(model_path="non_existent_folder/missing_model.pt")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert "models/best.pt" in str(e)
        print("\n[PASS] Missing model error handled cleanly with message:", str(e).splitlines()[0])

if __name__ == "__main__":
    print("Running automated verification suite...")
    test_health_endpoint()
    test_index_page()
    test_detect_image_upload()
    test_detect_invalid_file_extension()
    test_detect_missing_image_payload()
    test_detect_webcam_base64()
    test_clear_endpoint()
    test_missing_model_exception()
    print("\n==========================================")
    print("ALL AUTOMATED TESTS PASSED SUCCESSFULLY!  ")
    print("==========================================")
