# todo import
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

import os

from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# todo connection

GCS_CONN_ID = 'google_cloud_default'
SOURCE_BUCKET = 'dbt_datalake'
DESTINATION_BUCKET = 'bucket2-acidentes'
DESTINATION_OBJECT = 'teste_bucket/'
SOURCE_OBJECT = 'teste/*.csv'
LOCAL_FILE_SOURCE_BUCKET = 'fs_conn'
LOCAL_SOURCE_OBJECT = 'data/*.csv'

# todo default arguments
default_args = {
    'owner': 'Guilherme Arruda',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
#todo dafg definition
@dag(
    dag_id='Second_operator_dag',
    start_date=datetime(2025, 4, 7),
    max_active_runs=1,
    schedule_interval=timedelta(days=1),
    catchup=False,
    default_args=default_args,
    owner_links={"linkedin": "https://www.linkedin.com/in/arruda-guilherme/"},
    tags = ['second', 'dag', 'teste', 'operators']

)
# to do dag declaration, order of execution

def pipeline():
    @task()
    def move_files_to_processed(source_folder, destination_folder):
        for filename in os.listdir(source_folder):
            if filename.endswith('.csv'):
                source_file = os.path.join(source_folder, filename)
                destination_file = os.path.join(destination_folder, filename)

                # Move the file
                os.rename(source_file, destination_file)
                print(f"Moved: {source_file} to {destination_file}")
            else:
                print(f"Skipped: {filename} (not a CSV file)")



    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOCAL_SOURCE_OBJECT = os.path.join(BASE_DIR, 'include', 'data','staging', '*.csv')
    LOCAL_DESTINATION_PROCESSED_FOLDER = os.path.join(BASE_DIR, 'include', 'data','processed')
    LOCAL_SOURCE_FOLDER = os.path.join(BASE_DIR, 'include', 'data','staging')

    begin = EmptyOperator(task_id='begin')

    copy_from_local_to_gcs = LocalFilesystemToGCSOperator(
        task_id='copy_from_local_to_gcs',
        src=LOCAL_SOURCE_OBJECT,
        bucket=DESTINATION_BUCKET,
        dst=DESTINATION_OBJECT,
        gcp_conn_id=GCS_CONN_ID,
    )

    move_files_to_processed_task = move_files_to_processed(
        source_folder=LOCAL_SOURCE_FOLDER,
        destination_folder=LOCAL_DESTINATION_PROCESSED_FOLDER
    )

    

    end = EmptyOperator(task_id='end')
    

# instanciate the DAG

    begin >> copy_from_local_to_gcs >> move_files_to_processed_task >> end

pipeline()