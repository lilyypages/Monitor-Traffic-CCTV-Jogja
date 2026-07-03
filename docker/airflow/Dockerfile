FROM apache/airflow:2.9.1-python3.11

# Pin Airflow to base image version to prevent unwanted upgrades
RUN pip install --no-cache-dir "apache-airflow==2.9.1"

COPY requirements-airflow.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir "apache-airflow-providers-apache-spark<6.0"

# Fix: symlink airflow -> apache-airflow for entrypoint compatibility
RUN ln -sf /home/airflow/.local/bin/apache-airflow /home/airflow/.local/bin/airflow
