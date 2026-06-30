FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb-shm0 libxcb-xfixes0 libxcb-shape0 libxcb1 libx11-6 \
    libxext6 libgl1 libglib2.0-0 supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY docker/python/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
