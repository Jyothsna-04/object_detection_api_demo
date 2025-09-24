# object_detection.py
import cv2, requests
from ultralytics import YOLO

API = "http://localhost:5004/detections"
cap = cv2.VideoCapture(0)  # webcam (replace with IP cam if needed)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # nano version for speed
model.to("cpu")

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model.predict(frame, conf=0.4, verbose=False)
    detections = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = f"{model.names[cls]} {conf:.2f}"
        detections.append({"label": model.names[cls], "confidence": conf})

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Send to server
    if detections:
        requests.post(API, json={"detections": detections})

    cv2.imshow("Object Detection (YOLOv8)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
