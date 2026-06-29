import smtplib
from email.mime.text import MIMEText
from src.config import settings


def send_email(subject, body, to_addr=None):
    to_addr = to_addr or settings.ALERT_EMAIL_TO
    if not settings.SMTP_USER or not to_addr:
        print("[email] SMTP belum dikonfigurasi, skip")
        return False
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_addr
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, [to_addr], msg.as_string())
    return True


def notify_high_density(alert):
    if alert.get("total", 0) <= settings.DENSITY_THRESHOLD:
        return False
    subject = f"[ALERT] Kepadatan tinggi di {alert.get('camera_id')}"
    body = (
        f"Kepadatan melebihi threshold ({settings.DENSITY_THRESHOLD}).\n"
        f"Kamera: {alert.get('camera_id')}\n"
        f"Total: {alert.get('total')}\n"
        f"Waktu: {alert.get('timestamp')}"
    )
    return send_email(subject, body)


if __name__ == "__main__":
    send_email("Test Alert", "Email notifier aktif.")
