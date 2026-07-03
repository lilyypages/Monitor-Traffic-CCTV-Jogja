FROM apache/spark:3.5.1

USER root

RUN mkdir -p /tmp/checkpoints/density /tmp/checkpoints/traffic_count /tmp/checkpoints/aggregation /tmp/logs

COPY docker/spark/start_streaming.sh /app/start_streaming.sh
RUN chmod +x /app/start_streaming.sh

WORKDIR /app

CMD ["/bin/bash", "/app/start_streaming.sh"]
