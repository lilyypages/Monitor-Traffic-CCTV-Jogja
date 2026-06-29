import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch
from src.alerting import email_notifier
from src.alerting import telegram_bot


class TestEmailNotifier:
    def test_no_alert_below_threshold(self):
        alert = {"camera_id": "malioboro_01", "total": 1}
        assert email_notifier.notify_high_density(alert) is False

    @patch("src.alerting.email_notifier.send_email", return_value=True)
    def test_alert_above_threshold(self, mock_send):
        alert = {"camera_id": "malioboro_01", "total": 999, "timestamp": "2025-01-01 10:00:00"}
        assert email_notifier.notify_high_density(alert) is True
        mock_send.assert_called_once()


class TestTelegramBot:
    def test_format_alert_contains_fields(self):
        alert = {"camera_id": "malioboro_01", "total": 120, "timestamp": "2025-01-01 10:00:00"}
        text = telegram_bot.format_alert(alert)
        assert "malioboro_01" in text
        assert "120" in text
