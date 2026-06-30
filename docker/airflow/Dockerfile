FROM apache/airflow:2.9.1-python3.11

COPY requirements-airflow.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir apache-airflow-providers-apache-spark
