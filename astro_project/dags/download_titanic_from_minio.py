from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook  # For Airflow 2.5+
from datetime import datetime
import pandas as pd
import sqlalchemy

def download_from_minio():
    s3 = S3Hook(aws_conn_id='minio_default')
    bucket_name = 'titanic-dataset'
    object_key = 'Titanic-Dataset.csv'
    local_path = '/tmp/Titanic-Dataset.csv'  # changed to /tmp

    key = s3.get_key(key=object_key, bucket_name=bucket_name)
    key.download_file(local_path)
    print(f"Downloaded {object_key} to {local_path}")

def load_to_postgres():
    file_path = '/tmp/Titanic-Dataset.csv'  # changed to /tmp
    conn = BaseHook.get_connection('postgres_default')
    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    )
    df = pd.read_csv(file_path)
    df.to_sql('titanic_dataset', con=engine, if_exists='replace', index=False)
    print("Loaded data to Postgres")

default_args = {
    'start_date': datetime(2025, 6, 13),
    'owner': 'airflow',
}

with DAG(
    dag_id='minio_to_postgres_titanic',
    schedule=None,
    default_args=default_args,
    catchup=False,
) as dag:

    download_task = PythonOperator(
        task_id='download_from_minio',
        python_callable=download_from_minio,
    )

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres,
    )

    download_task >> load_task
