FROM bitnami/spark:3.5.1

USER root

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src/spark/ /opt/spark-app/src/spark/

USER 1001
