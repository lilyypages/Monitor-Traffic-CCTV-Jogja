FROM apache/spark:3.5.1

USER root

RUN apt-get update && apt-get install -y curl python3-pip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY src/spark/ /opt/spark-app/src/spark/

USER spark
