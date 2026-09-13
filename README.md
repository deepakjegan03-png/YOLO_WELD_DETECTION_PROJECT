# YOLO Object Detection Web Application

A complete, beginner-friendly, and professional object-detection web application built with **Flask**, **Ultralytics YOLO**, **OpenCV**, and a modern **HTML5/Bootstrap 5** frontend.

---

## 📁 Project Structure

```
Weld_Project/
│
├── app.py                     # Flask web server, API routes, file handling
├── config.py                  # Project settings, thresholds, upload limits
├── requirements.txt           # Python dependencies
├── README.md                  # Beginner guide & troubleshooting
│
├── models/
│   └── best.pt                # Your trained YOLO model weights file
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling, animations & layout
│   ├── js/
│   │   └── script.js          # Interactive frontend logic & camera streaming
│   └── results/               # Generated detection images with bounding boxes
│
├── templates/
│   └── index.html             # Responsive dashboard user interface
│
├── uploads/                   # Temporary uploaded images
│
└── utils/
    ├── __init__.py            # Package initializer
    └── detector.py            # YOLODetector inference engine & box rendering
```

---

## 🚀 Beginner-Friendly Setup (Windows)

Follow these exact steps to run the application on your computer:

### STEP 1: Open the project folder
Open File Explorer and navigate to your project directory:
```
c:\Users\acer\OneDrive\Documents - Copy\Weld_Project
```

### STEP 2: Open Command Prompt or PowerShell
Press `Win + R`, type `cmd` (or `powershell`), and press Enter. Navigate to your project folder:
```powershell
cd "c:\Users\acer\OneDrive\Documents - Copy\Weld_Project"
```

### STEP 3: Create a Python virtual environment
```powershell
python -m venv venv
```

### STEP 4: Activate the virtual environment
On Windows:
```powershell
venv\Scripts\activate
```
*(If you see `(venv)` at the beginning of your command line, the virtual environment is active.)*

### STEP 5: Install required packages
```powershell
pip install -r requirements.txt
```

### STEP 6: Place your YOLO model
Ensure your trained YOLO `.pt` model weights file is located at:
```
models/best.pt
```
*(If it is named something else, copy and rename it to `models/best.pt`, or update `MODEL_PATH` in `config.py`.)*

### STEP 7: Run the application
```powershell
python app.py
```

### STEP 8: Open in your web browser
Open your browser (Google Chrome, Microsoft Edge, Firefox, or Brave) and navigate to:
```
http://127.0.0.1:5000
```
or:
```
http://localhost:5000
```

---

## 🎯 How Features Work

### 1. Image Upload Detection
1. Drag and drop an image (`.jpg`, `.jpeg`, `.png`, `.webp`) into the **Upload Image** box, or click **browse**.
2. A preview of the original image appears instantly.
3. Adjust the **Confidence Threshold** slider (default is 25%).
4. Click **Detect Objects**.
5. The backend runs YOLO inference, draws colored bounding boxes, labels, and confidence percentages.
6. The side-by-side comparison, summary metrics, and detection table appear automatically without reloading the page.

### 2. Live Browser Webcam Detection
1. Click **Start Camera**.
2. Your browser will prompt: *"Allow this site to use your camera?"* — Click **Allow**.
3. Position your object in front of the camera using the live video feed.
4. Click **Capture Image** to freeze the desired frame.
5. Click **Detect**.
6. The captured frame is sent to Flask via Base64, processed with YOLO, and displayed with bounding boxes, confidence scores, and detection rows.
7. Click **Stop Camera** whenever you are done.

### 3. Confidence Threshold Control
- Use the slider at the top of the dashboard to choose any confidence cutoff between **10%** and **95%**.
- Detections with confidence below your selected threshold will be filtered out.

### 4. Reset Button
- Click the **Reset** button in the header at any time.
- It immediately turns off the webcam, clears image previews, wipes the results table, resets counters, and clears temporary server cache files without needing to restart the Flask server.

---

## 🛠️ Troubleshooting Guide

### 1. "Python is not recognized as an internal or external command"
- **Cause**: Python is not added to your Windows PATH environment variable.
- **Fix**: Re-run the Python installer, check the box **"Add Python to PATH"**, and restart your terminal. Alternatively, invoke Python with `py app.py`.

### 2. "pip is not recognized"
- **Cause**: pip was not installed or PATH is missing the `Scripts` directory.
- **Fix**: Run `python -m ensurepip --upgrade` or use `python -m pip install -r requirements.txt`.

### 3. "ModuleNotFoundError: No module named 'flask'" (or 'ultralytics', 'cv2')
- **Cause**: Dependencies were installed in a different environment or venv is not activated.
- **Fix**: Ensure your virtual environment is active (`venv\Scripts\activate`), then run `pip install -r requirements.txt`.

### 4. "YOLO model not found" / "models/best.pt does not exist"
- **Cause**: The weights file is missing from the `models/` directory.
- **Fix**: Copy your trained YOLO weights file into `models/best.pt`. If your model file is located in `runs/detect/.../weights/best.pt`, copy it into `models/best.pt`.

### 5. "Camera permission denied"
- **Cause**: Browser blocked webcam access.
- **Fix**: In your browser's address bar, click the **Camera / Lock icon** next to `http://127.0.0.1:5000` and select **"Allow"** for Camera permissions, then refresh the page.

### 6. "Camera does not open" / "No camera device found"
- **Cause**: Another app (Zoom, Teams, Skype, or an OpenCV script) has locked the webcam.
- **Fix**: Close other apps using the webcam. In Windows Settings > Privacy & Security > Camera, ensure **"Let desktop apps access your camera"** is enabled.

### 7. "Address already in use" / "Port 5000 already in use"
- **Cause**: Another instance of Flask or another service is already using port 5000.
- **Fix**: Change `SERVER_PORT = 5001` in `config.py` and run `python app.py` again.

### 8. OpenCV installation issue ("ImportError: DLL load failed")
- **Cause**: Missing Windows Visual C++ Redistributable.
- **Fix**: Download and install the free **Visual C++ Redistributable (x64)** from Microsoft's official site: [https://aka.ms/vs/17/release/vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe).

### 9. Ultralytics installation issue / PyTorch conflict
- **Cause**: Conflicting PyTorch CPU/CUDA wheels.
- **Fix**: Run `pip install --upgrade pip` followed by `pip install ultralytics --extra-index-url https://download.pytorch.org/whl/cpu`.
