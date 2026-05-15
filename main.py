import cv2
import supervision as sv

from ultralytics import YOLO

from src.stream.youtube_stream import get_youtube_stream_url
from src.tracking.vehicle_tracking import track_objects

youtube_url = "https://www.youtube.com/live/PjwEkfbM8zU"

stream_url = get_youtube_stream_url(youtube_url)

cap = cv2.VideoCapture(stream_url)

model = YOLO("yolov8n.pt")

vehicle_classes = [2, 3, 5, 7]

counted_ids = set()
total_count = 0

box_annotator = sv.BoxAnnotator()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(results)

    detections = track_objects(detections)


    for i, class_id in enumerate(detections.class_id):

        if class_id in vehicle_classes:

            tracker_id = detections.tracker_id[i]

            if tracker_id is not None:

                if tracker_id not in counted_ids:
                    counted_ids.add(tracker_id)
                    total_count += 1

    annotated_frame = box_annotator.annotate(
        scene=frame,
        detections=detections
    )

    cv2.putText(
        annotated_frame,
        f"Total Vehicles: {total_count}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.imshow("Traffic Monitoring", annotated_frame)

    print("Total Vehicles:", total_count)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()