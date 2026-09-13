Build a complete, professional object-detection web application using my existing YOLO model.

IMPORTANT:
- The application must run on my LOCALHOST.
- Do NOT make this a cloud-only application.
- Do NOT require Streamlit.
- Use Flask as the backend.
- Use HTML, CSS and JavaScript for the frontend.
- The application must support BOTH image upload and live webcam detection.
- The application should be easy for a beginner to run on Windows.
- Give me the complete project structure and all required source code.
- Make sure the application works with my existing YOLO .pt model.

==================================================
1. PROJECT OBJECTIVE
==================================================

Create a web application for object detection using YOLO.

The user should be able to:

A. Upload an image from the computer
B. Open the computer webcam
C. Capture an image/frame from the webcam
D. Send the image to the backend
E. Run YOLO object detection
F. Display the detected image with bounding boxes
G. Display detected class names
H. Display confidence scores
I. Display the total number of detected objects
J. Clear/reset the current result
K. Use the application again without restarting the server

The application should have a clean, modern and professional UI suitable for a college project/demo.

==================================================
2. TECHNOLOGY STACK
==================================================

Backend:
- Python
- Flask
- Ultralytics YOLO
- OpenCV
- NumPy
- Pillow where necessary

Frontend:
- HTML5
- CSS3
- JavaScript
- Bootstrap 5 or clean custom CSS

Model:
- My existing YOLO .pt model

The code should be compatible with a normal Windows Python environment.

==================================================
3. REQUIRED PROJECT STRUCTURE
==================================================

Create the following structure:

project/
│
├── app.py
├── requirements.txt
├── README.md
├── config.py
│
├── models/
│   └── best.pt
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── results/
│
├── templates/
│   └── index.html
│
├── uploads/
│
└── utils/
    ├── __init__.py
    └── detector.py

IMPORTANT:
- best.pt is my YOLO trained model.
- Make the model path configurable.
- Do not hard-code an invalid model path.
- If best.pt is not present, display a clear error message explaining where it should be placed.

==================================================
4. BACKEND ARCHITECTURE
==================================================

Create Flask application in app.py.

The backend should have routes similar to:

GET /
    -> Render the main web page.

POST /detect
    -> Accept uploaded image.
    -> Save image temporarily.
    -> Run YOLO inference.
    -> Draw bounding boxes.
    -> Save the result.
    -> Return JSON containing:
       - result image URL
       - detected objects
       - class names
       - confidence
       - bounding box coordinates
       - total detections

POST /detect_webcam
    -> Accept an image captured from browser webcam as Base64.
    -> Convert Base64 image to OpenCV image.
    -> Run YOLO inference.
    -> Return detection result.

POST /clear
    -> Clear temporary result files if required.

Also create a health/status route:

GET /health
    -> Return JSON:
       {
         "status": "running"
       }

==================================================
5. YOLO DETECTOR
==================================================

Create:

utils/detector.py

Create a detector class such as:

YOLODetector

Responsibilities:

- Load the YOLO model only once when the Flask application starts.
- Accept an image.
- Run inference.
- Extract detections.
- Draw bounding boxes.
- Display class names.
- Display confidence percentage.
- Return processed image and structured detection data.

Example detection format:

[
    {
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.94,
        "bbox": {
            "x1": 100,
            "y1": 120,
            "x2": 300,
            "y2": 450
        }
    }
]

Do NOT assume my classes are person/car/etc.

Read class names directly from the loaded YOLO model.

==================================================
6. MODEL CONFIGURATION
==================================================

Create config.py.

Use something similar to:

MODEL_PATH = "models/best.pt"
CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 640

Make these values easy to change.

The user should be able to change confidence threshold later.

==================================================
7. IMAGE UPLOAD FEATURE
==================================================

On the frontend create an:

"Upload Image"

section.

Allow the user to select:

- JPG
- JPEG
- PNG
- WEBP

After selecting the image:

1. Show image preview.
2. Show "Detect Objects" button.
3. Send the image to Flask using fetch().
4. Show a loading indicator.
5. Run YOLO detection.
6. Display processed image.
7. Display detection results.

The UI should not reload the entire page.

Use AJAX/fetch API.

==================================================
8. WEBCAM FEATURE
==================================================

Create a separate:

"Webcam Detection"

section.

Add buttons:

- Start Camera
- Capture Image
- Detect
- Stop Camera

When the user clicks:

"Start Camera"

use browser JavaScript:

navigator.mediaDevices.getUserMedia()

to request webcam access.

IMPORTANT:
Do not access the webcam directly from Python/OpenCV when the goal is browser webcam access.

The browser webcam should be accessed using JavaScript.

Show the live camera stream inside a video element.

When the user clicks:

"Capture Image"

capture the current webcam frame using:

HTML canvas

Convert the canvas image into Base64.

Send it to Flask.

Flask should decode the Base64 image and run YOLO.

Return the processed image.

Display the processed detection image.

==================================================
9. WEBCAM UI
==================================================

Create a professional webcam panel:

------------------------------------------
|          Webcam Detection              |
|                                        |
|       [ Live Camera Preview ]          |
|                                        |
| [Start Camera] [Capture] [Stop Camera] |
|                                        |
|       Detection Result                 |
|       [Processed Image]                |
------------------------------------------

Show useful messages:

"Camera permission required"

"Camera started"

"Image captured"

"Detecting objects..."

"Detection completed"

"Camera stopped"

Handle browser camera permission errors gracefully.

==================================================
10. DETECTION RESULT PANEL
==================================================

After detection, show:

Detection Results

Total Objects Detected: 5

Then display a table:

------------------------------------------------
| # | Object | Confidence | Bounding Box       |
------------------------------------------------
| 1 | Class1 | 95.2%      | (100,120,300,400) |
| 2 | Class2 | 88.6%      | (50,80,200,300)  |
------------------------------------------------

Do not hard-code class names.

Use the actual class names from the YOLO model.

==================================================
11. CONFIDENCE THRESHOLD
==================================================

Add a confidence threshold control.

Example:

Confidence Threshold
[ 25% ]

The user should be able to change it.

Recommended range:

0.10 to 0.95

Default:

0.25

Send the selected confidence threshold to the backend.

The backend must validate the value.

==================================================
12. FRONTEND DESIGN
==================================================

Create a modern dashboard.

Header:

"YOLO Object Detection"

Subtitle:

"Detect objects using image upload or webcam"

Main layout:

-------------------------------------------------
|              YOLO OBJECT DETECTION            |
|       Image & Webcam Detection Dashboard      |
-------------------------------------------------

Two main cards:

CARD 1:
Upload Image

CARD 2:
Webcam Detection

Below them:

Detection Result

Detection Statistics

Detection Table

Use responsive design.

The application must work on:

- Desktop
- Laptop
- Tablet
- Mobile browser

Use a professional color scheme but keep the design simple.

Do not make the UI unnecessarily complicated.

==================================================
13. IMAGE PREVIEW
==================================================

Before detection:

Show:

"Original Image"

After detection:

Show:

"Detection Result"

If possible, display them side by side on desktop.

On mobile, stack them vertically.

==================================================
14. LOADING STATE
==================================================

When YOLO is processing:

Show:

"Detecting objects..."

with a spinner/loading animation.

Disable the Detect button during processing.

After completion:

Enable the button again.

==================================================
15. ERROR HANDLING
==================================================

Handle all common errors.

Examples:

No image selected
Invalid image format
Image too large
Model not found
YOLO inference error
Invalid confidence value
Camera permission denied
Camera not available
Invalid Base64 image
Server error

Show friendly messages to the user.

Do not expose Python stack traces in the frontend.

Print useful debugging information in the Flask terminal.

==================================================
16. FILE VALIDATION
==================================================

Only allow:

.png
.jpg
.jpeg
.webp

Use Flask secure filename handling.

Create reasonable file size limit.

Example:

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

Display a friendly error if the file is too large.

==================================================
17. RESULT IMAGE
==================================================

YOLO should draw:

- Bounding rectangle
- Class name
- Confidence score

Example:

ClassName 94%

The result should be saved inside:

static/results/

Use unique filenames to avoid overwriting previous results.

==================================================
18. API RESPONSE
==================================================

The /detect endpoint should return JSON similar to:

{
    "success": true,
    "result_image": "/static/results/result_123.jpg",
    "total_detections": 3,
    "detections": [
        {
            "class_id": 0,
            "class_name": "example",
            "confidence": 0.94,
            "bbox": {
                "x1": 100,
                "y1": 120,
                "x2": 300,
                "y2": 400
            }
        }
    ]
}

For errors:

{
    "success": false,
    "error": "Readable error message"
}

==================================================
19. SECURITY
==================================================

Implement basic security practices:

- secure_filename()
- allowed extensions
- file size limit
- validate uploaded files
- validate Base64 webcam data
- don't execute uploaded files
- don't expose internal server paths
- don't expose stack traces to the browser

==================================================
20. PERFORMANCE
==================================================

Important:

Load YOLO model only once.

Do NOT load:

YOLO("best.pt")

for every request.

Instead load the model when the Flask application starts.

Reuse the loaded model.

Use an appropriate image size.

Keep the application simple enough to run on a normal laptop.

==================================================
21. LOCALHOST
==================================================

The application must run using:

python app.py

The Flask server should run on:

http://127.0.0.1:5000

or:

http://localhost:5000

Show the URL clearly in the terminal.

For example:

=========================================
YOLO OBJECT DETECTION SERVER
=========================================
Server running at:
http://127.0.0.1:5000
=========================================

==================================================
22. REQUIREMENTS.TXT
==================================================

Create requirements.txt containing the required packages.

Include appropriate packages for:

- Flask
- ultralytics
- opencv-python
- numpy
- Pillow

Do not include unnecessary packages.

==================================================
23. WINDOWS SETUP
==================================================

Create a beginner-friendly README.md.

Explain exactly:

STEP 1:
Open the project folder.

STEP 2:
Open Command Prompt/PowerShell.

STEP 3:
Create virtual environment:

python -m venv venv

STEP 4:
Activate:

Windows:

venv\Scripts\activate

STEP 5:
Install packages:

pip install -r requirements.txt

STEP 6:
Put my YOLO model here:

models/best.pt

STEP 7:
Run:

python app.py

STEP 8:
Open browser:

http://127.0.0.1:5000

==================================================
24. TROUBLESHOOTING
==================================================

README must include solutions for:

Python not recognized
pip not recognized
ModuleNotFoundError
YOLO model not found
Camera permission denied
Camera does not open
Port 5000 already in use
OpenCV installation issue
Ultralytics installation issue

Keep explanations beginner-friendly.

==================================================
25. CAMERA SECURITY / LOCALHOST
==================================================

The webcam must work on localhost.

Use:

navigator.mediaDevices.getUserMedia()

and explain that the browser may ask for camera permission.

Do not require HTTPS for localhost unless the browser specifically requires it.

==================================================
26. UI FEATURES
==================================================

Add:

- Navigation/header
- Upload tab
- Webcam tab
- Result section
- Detection count
- Confidence threshold
- Reset button
- Loading indicator
- Error alert
- Success alert

Use icons where useful.

==================================================
27. RESET BUTTON
==================================================

Create:

"Reset"

button.

When clicked:

- Clear uploaded image
- Clear webcam result
- Clear detection table
- Reset detection count
- Hide result image
- Stop webcam if running
- Reset messages

==================================================
28. IMPORTANT BEGINNER REQUIREMENT
==================================================

Do not give me only partial code.

Generate the COMPLETE working project.

I want:

1. app.py
2. config.py
3. utils/detector.py
4. utils/__init__.py
5. templates/index.html
6. static/css/style.css
7. static/js/script.js
8. requirements.txt
9. README.md

All files must work together.

==================================================
29. DO NOT USE PLACEHOLDERS
==================================================

Do not write:

# add your code here

or:

# implement this yourself

or:

TODO

Provide the actual working code.

The only external file expected from me should be:

models/best.pt

==================================================
30. YOLO VERSION COMPATIBILITY
==================================================

Use the current Ultralytics YOLO Python API.

Prefer:

from ultralytics import YOLO

model = YOLO(MODEL_PATH)

Do not use obsolete YOLO APIs.

==================================================
31. DETECTION FLOW
==================================================

IMAGE UPLOAD FLOW:

User
 ↓
Upload Image
 ↓
Browser Preview
 ↓
Click Detect
 ↓
JavaScript fetch()
 ↓
Flask /detect
 ↓
YOLO Model
 ↓
Object Detection
 ↓
Bounding Boxes
 ↓
JSON Response
 ↓
Frontend
 ↓
Detection Result + Table

WEBCAM FLOW:

User
 ↓
Start Camera
 ↓
Browser getUserMedia()
 ↓
Live Video
 ↓
Capture Frame
 ↓
Canvas
 ↓
Base64 Image
 ↓
Flask /detect_webcam
 ↓
YOLO Model
 ↓
Detection
 ↓
JSON Response
 ↓
Frontend
 ↓
Result Image + Detection Table

==================================================
32. CODE QUALITY
==================================================

Use:

- functions
- classes where useful
- clear variable names
- comments for important sections
- error handling
- modular code

Avoid unnecessary complexity.

The code should be understandable by a beginner learning Python and Flask.

==================================================
33. FINAL TESTING
==================================================

After generating the project, verify:

TEST 1:
Server starts successfully.

TEST 2:
Home page loads.

TEST 3:
Image upload works.

TEST 4:
YOLO detects objects.

TEST 5:
Bounding boxes appear.

TEST 6:
Confidence scores appear.

TEST 7:
Detection table appears.

TEST 8:
Camera permission works.

TEST 9:
Webcam starts.

TEST 10:
Webcam capture works.

TEST 11:
Captured frame reaches Flask.

TEST 12:
YOLO detects objects from webcam frame.

TEST 13:
Reset works.

TEST 14:
Invalid image produces friendly error.

TEST 15:
Missing model produces useful error.

==================================================
34. IMPORTANT OUTPUT FROM ANTIGRAVITY
==================================================

After building the application, show me:

1. Complete folder structure
2. Complete code for every file
3. Installation commands
4. Run commands
5. Localhost URL
6. How to place best.pt
7. How image upload works
8. How webcam works
9. How to change confidence threshold
10. Troubleshooting instructions

Most importantly:

BUILD THE ACTUAL WORKING APPLICATION, NOT JUST A DESIGN MOCKUP.

The final application must run locally using:

python app.py

and open at:

http://127.0.0.1:5000