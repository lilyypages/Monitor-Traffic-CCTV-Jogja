import threading
import time

active_cameras = {}
camera_threads = {}

def start_camera(camera_id, process_fn):
    if camera_id in active_cameras:
        return
    active_cameras[camera_id] = True
    thread = threading.Thread(target=process_fn, daemon=True)
    camera_threads[camera_id] = thread
    thread.start()
    return thread

def stop_camera(camera_id):
    active_cameras[camera_id] = False

def is_active(camera_id):
    return active_cameras.get(camera_id, False)

def get_active_count():
    return len([c for c in active_cameras if active_cameras[c]])

def switch_camera(old_id, new_id, process_fn):
    stop_camera(old_id)
    time.sleep(0.5)
    return start_camera(new_id, process_fn)
