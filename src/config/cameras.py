CAMERAS = {
    "malioboro_01": {
        "name": "Malioboro - Plaza",
        "url": "https://www.youtube.com/watch?v=q7ZX2tSFEDg",
        "lat": -7.792,
        "lon": 110.365
    },
    "malioboro_02": {
        "name": "Malioboro - Utara Inna",
        "url": "https://www.youtube.com/live/ozAEmr_r5Pg",
        "lat": -7.791,
        "lon": 110.366
    }
}

def get_camera(camera_id="malioboro_01"):
    return CAMERAS.get(camera_id)

def get_all_cameras():
    return list(CAMERAS.keys())
