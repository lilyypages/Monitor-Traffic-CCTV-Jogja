from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def run_ml_training():
    from src.ml.train import run_training
    run_training()

with DAG(
    'traffic_weekly_ml_retrain',
    default_args=default_args,
    schedule_interval='0 6 * * 0',
    catchup=False,
    tags=['traffic', 'ml'],
) as dag:

    prepare_data = SparkSubmitOperator(
        task_id='prepare_training_data',
        application='/opt/spark-app/src/spark/batch/prediction_input.py',
        conn_id='spark_default',
        verbose=True,
    )

    train_models = PythonOperator(
        task_id='train_ml_models',
        python_callable=run_ml_training,
    )

    prepare_data >> train_models
