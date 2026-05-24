import supervision as sv

tracker = sv.ByteTrack()

def track_objects(detections):
    return tracker.update_with_detections(detections)