from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

SERVICES = [
    ('check_postgres', "pg_isready -h postgres -U postgres"),
    ('check_kafka', "echo 'test' | nc -w 2 kafka 9092 && echo OK || echo FAIL"),
    ('check_spark_master', "curl -sf http://spark-master:8080 && echo OK || echo FAIL"),
    ('check_grafana', "curl -sf http://grafana:3000/api/health && echo OK || echo FAIL"),
]

def check_service(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    print(output)
    if 'FAIL' in output or result.returncode != 0:
        raise Exception(f"Service check failed: {output}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'traffic_pipeline_health_check',
    default_args=default_args,
    schedule_interval='*/30 * * * *',
    catchup=False,
    tags=['traffic', 'monitoring'],
) as dag:

    for task_id, cmd in SERVICES:
        PythonOperator(
            task_id=task_id,
            python_callable=check_service,
            op_kwargs={'command': cmd},
        )
