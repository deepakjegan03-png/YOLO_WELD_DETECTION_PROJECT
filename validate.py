from ultralytics import YOLO
 
model = YOLO("runs/detect/yolo weld detection project/weld_yolo_training/weights/best.pt")
 
metrics = model.val(data="data.yaml")
print(metrics)