import time
from ultralytics import YOLO
import cv2
 
model = YOLO("runs/detect/yolo weld detection project/weld_yolo_training/weights/best.pt")          # or the full runs/... path
 
image = cv2.imread("")
 
start = time.time()
results = model(image)
end = time.time()
 
latency = end - start
print("Inference Time:", latency, "seconds")