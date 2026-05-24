import cv2
import supervision as sv
import time
import numpy as np
from collections import defaultdict
from datetime import datetime

from src.ingestion.youtube_stream import get_youtube_stream_url
from src.processing.tracking.vehicle_tracking import track_objects
from src.config.cameras import get_camera
from src.storage.logger import save_data, create_table
from src.utils.helpers import get_logger, get_error_logger

camera = get_camera("malioboro_01")
CAMERA_ID = "malioboro_01"
YOUTUBE_URL = camera["url"]
SAVE_INTERVAL = 10

model = None
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

CLASS_NAMES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck", 0: "person"}
VEHICLE_CLASSES = [2, 3, 5, 7]

logger = get_logger()
error_logger = get_error_logger()


def load_model():
    global model
    from ultralytics import YOLO
    model = YOLO("models/yolov8n.pt")
    logger.info("Model YOLOv8 loaded")


def process_frame(frame, counted_ids, total_count, frame_count):
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)

    class_counts = defaultdict(int)
    for cls_id in detections.class_id:
        class_counts[int(cls_id)] += 1

    mask = np.isin(detections.class_id, list(CLASS_NAMES.keys()))
    detections = detections[mask]

    if len(detections) > 0:
        detections = track_objects(detections)

    for i, class_id in enumerate(detections.class_id):
        if int(class_id) in VEHICLE_CLASSES:
            tracker_id = detections.tracker_id[i]
            if tracker_id is not None and tracker_id not in counted_ids:
                counted_ids.add(tracker_id)
                total_count += 1

    annotated = frame.copy()

    if len(detections) > 0:
        labels = [
            f"{CLASS_NAMES.get(int(cls_id), 'unknown')} #{tid}"
            for cls_id, tid in zip(detections.class_id, detections.tracker_id)
        ]
        annotated = box_annotator.annotate(scene=annotated, detections=detections)
        annotated = label_annotator.annotate(scene=annotated, detections=detections, labels=labels)

    return annotated, class_counts, total_count, detections


def main():
    logger.info("=" * 50)
    logger.info(f"Traffic Monitor dimulai - {CAMERA_ID}")
    logger.info(f"Lokasi: {camera['name']}")
    logger.info("=" * 50)

    load_model()
    create_table()

    logger.info(f"Mengambil stream dari YouTube...")
    stream_url = get_youtube_stream_url(YOUTUBE_URL)
    cap = cv2.VideoCapture(stream_url)

    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 30000)
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 30000)

    if not cap.isOpened():
        error_logger.error("Gagal membuka stream YouTube")
        return

    logger.info("Stream berhasil dibuka")

    counted_ids = set()
    total_count = 0
    frame_count = 0
    last_save_time = time.time()
    fps_start = time.time()
    fps_frames = 0
    current_fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                error_logger.warning("Frame gagal dibaca, reconnect...")
                time.sleep(1)
                cap = cv2.VideoCapture(get_youtube_stream_url(YOUTUBE_URL))
                continue

            frame_count += 1
            fps_frames += 1

            annotated, class_counts, total_count, detections = process_frame(
                frame, counted_ids, total_count, frame_count
            )

            fps_elapsed = time.time() - fps_start
            if fps_elapsed >= 1.0:
                current_fps = fps_frames / fps_elapsed
                fps_frames = 0
                fps_start = time.time()

            active_objects = len(detections)

            overlay_text = [
                f"Total Kendaraan: {total_count}",
                f"FPS: {current_fps:.1f}",
                f"Aktif: {active_objects} objek",
                f"Frame: {frame_count}"
            ]
            for i, text in enumerate(overlay_text):
                cv2.putText(annotated, text, (15, 30 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow(f"Traffic Monitor - {camera['name']}", annotated)

            if time.time() - last_save_time >= SAVE_INTERVAL:
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "camera_id": CAMERA_ID,
                    "car": class_counts.get(2, 0),
                    "motorcycle": class_counts.get(3, 0),
                    "bus": class_counts.get(5, 0),
                    "truck": class_counts.get(7, 0),
                    "person": class_counts.get(0, 0),
                    "total": total_count,
                    "fps": round(current_fps, 1)
                }
                save_data(data)
                logger.info(
                    f"Data | Total:{total_count} | Car:{data['car']} Motor:{data['motorcycle']} "
                    f"Bus:{data['bus']} Truck:{data['truck']} Person:{data['person']} "
                    f"FPS:{current_fps:.1f}"
                )
                last_save_time = time.time()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                logger.info("Stream dihentikan oleh user")
                break

    except KeyboardInterrupt:
        logger.info("Program dihentikan")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info(f"Sesi selesai. Total kendaraan terhitung: {total_count}")


if __name__ == "__main__":
    main()
