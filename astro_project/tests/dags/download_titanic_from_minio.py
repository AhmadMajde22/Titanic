from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime


def download_titanic_dataset():
    # Initialize S3Hook with your MinIO connection
    s3 = S3Hook(aws_conn_id='minio_default')

    bucket_name = 'titanic-dataset'
    object_key = 'Titanic-Dataset.csv'
    local_path = '/tmp/Titanic-Dataset.csv'

    # Download file from MinIO bucket to local path
    s3.get_key(key=object_key, bucket_name=bucket_name).download_file(local_path)
    print(f"✅ Downloaded {object_key} from bucket {bucket_name} to {local_path}")


default_args = {
    'start_date': datetime(2025, 6, 12),
    'owner': 'airflow',
}

with DAG(
    dag_id='download_titanic_from_minio',
    schedule=None,
    default_args=default_args,
    catchup=False,
    description='Download Titanic dataset from MinIO using S3Hook',
    tags=['minio', 's3', 'titanic'],
) as dag:

    download_task = PythonOperator(
        task_id='download_titanic_dataset',
        python_callable=download_titanic_dataset,
    )
