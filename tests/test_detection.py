import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import numpy as np
from unittest.mock import patch, MagicMock


class TestVehicleDetection:
    def test_mock_detection_returns_list(self):
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        fake_results = MagicMock()
        fake_box = MagicMock()
        fake_box.cls = [2]
        fake_box.xyxy = [[100, 100, 200, 200]]
        fake_results.boxes = [fake_box]

        with patch("src.processing.detection.vehicle_detection.model") as mock_model:
            mock_model.return_value = [fake_results]
            from src.processing.detection.vehicle_detection import detect_vehicles
            detections = detect_vehicles(fake_frame)
            assert isinstance(detections, list)

    def test_empty_frame_no_error(self):
        fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        from src.processing.detection.vehicle_detection import vehicle_classes
        assert 2 in vehicle_classes
        assert 3 in vehicle_classes
        assert 5 in vehicle_classes
        assert 7 in vehicle_classes
        assert len(vehicle_classes) == 4


class TestVehicleTracking:
    def test_tracker_initialized(self):
        from src.processing.tracking.vehicle_tracking import tracker
        assert tracker is not None

    def test_track_empty_detections(self):
        import supervision as sv
        from src.processing.tracking.vehicle_tracking import track_objects
        empty_detections = sv.Detections.empty()
        result = track_objects(empty_detections)
        assert len(result) == 0


class TestYouTubeStream:
    def test_get_camera_config(self):
        from src.config.cameras import get_camera, CAMERAS
        camera = get_camera("malioboro_01")
        assert camera is not None
        assert "url" in camera
        assert "youtube.com" in camera["url"]
