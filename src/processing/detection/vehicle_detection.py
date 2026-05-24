from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")

vehicle_classes = [2, 3, 5, 7]
# 2=car
# 3=motorcycle
# 5=bus
# 7=truck

def detect_vehicles(frame):
    results = model(frame)

    detections = []

    for result in results:
        boxes = result.boxes

        for box in boxes:
            cls = int(box.cls[0])

            if cls in vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "class": cls,
                    "bbox": [x1, y1, x2, y2]
                })

    return detections