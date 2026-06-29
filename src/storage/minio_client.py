import io
import json
from minio import Minio
from src.config import settings


def get_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


def ensure_bucket(bucket):
    client = get_client()
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    return client


def upload_json(bucket, object_name, data):
    client = ensure_bucket(bucket)
    payload = json.dumps(data).encode("utf-8")
    client.put_object(
        bucket,
        object_name,
        io.BytesIO(payload),
        length=len(payload),
        content_type="application/json",
    )
    return f"{bucket}/{object_name}"


if __name__ == "__main__":
    path = upload_json(
        "traffic-raw",
        "frames/test.json",
        {"camera_id": "malioboro_01", "total": 93},
    )
    print("uploaded:", path)
