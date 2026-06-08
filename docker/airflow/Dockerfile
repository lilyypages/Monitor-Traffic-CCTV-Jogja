FROM apache/airflow:2.9.1-python3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt

RUN pip install --no-cache-dir --user apache-airflow-providers-apache-spark
