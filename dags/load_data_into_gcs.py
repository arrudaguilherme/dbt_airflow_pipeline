# todo import
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

import os
import pandas as pd
import glob


from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

# todo connection

GCS_CONN_ID = 'google_cloud_default'
SOURCE_BUCKET = 'dbt_datalake'
DESTINATION_BUCKET = 'bucket2-acidentes'
DESTINATION_OBJECT = 'staging/'
DESTINATION_OBJECT_PROCESSED = 'processed/'
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
    dag_id='load_data_into_gcs',
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
    def read_and_save_csv_str_column(input_directory, output_directory):
        # Use glob para buscar todos os arquivos CSV no diretório
        csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
        
        for file_path in csv_files:
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_directory, file_name)
            
            
            df = pd.read_csv(file_path, encoding='utf-8', sep=';', dtype={'id': str, 'km': str}, decimal=',')
            
            
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            
            
            df['id'] = df['id'].astype(str)  
            df['km'] = pd.to_numeric(df['km'], errors='coerce')  
            df['data_inversa'] = pd.to_datetime(df['data_inversa'], errors='coerce', dayfirst=True)  
            
            
            df.to_csv(output_path, index=False, sep=';', encoding='utf-8')
            
            print(f"Arquivo lido e salvo com sucesso em {output_path}")
        
        return len(csv_files)


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

    file_paths = glob.glob(LOCAL_SOURCE_OBJECT)

    begin = EmptyOperator(task_id='begin')

    read_and_save_csv_str_column_task = read_and_save_csv_str_column(
        input_directory=LOCAL_SOURCE_FOLDER,
        output_directory=LOCAL_SOURCE_FOLDER
    )

    copy_from_local_to_gcs = LocalFilesystemToGCSOperator(
        task_id='copy_from_local_to_gcs',
        src=LOCAL_SOURCE_OBJECT,
        bucket=DESTINATION_BUCKET,
        dst=DESTINATION_OBJECT,
        gcp_conn_id=GCS_CONN_ID,
    )

    #declare task
    move_files_to_processed_task = move_files_to_processed(
        source_folder=LOCAL_SOURCE_FOLDER,
        destination_folder=LOCAL_DESTINATION_PROCESSED_FOLDER
    )

    insert_gcs_to_bigquery = GCSToBigQueryOperator(
        task_id='insert_gcs_to_bigquery',
        bucket=DESTINATION_BUCKET,
        source_objects=[f'{DESTINATION_OBJECT}*.csv'],
        destination_project_dataset_table='dbt-warehouse-455922.acidentes_brasil.raw_acidentes_brasil',
        source_format='CSV',
        field_delimiter=';',
        skip_leading_rows=1,
        write_disposition='WRITE_APPEND',
        gcp_conn_id=GCS_CONN_ID,
    )

    move_files_gcs_to_processed_gcs = GCSToGCSOperator(
        task_id='move_files_gcs_to_processed_gcs',
        source_bucket=DESTINATION_BUCKET,
        source_object=DESTINATION_OBJECT,
        destination_bucket=DESTINATION_BUCKET,
        destination_object=DESTINATION_OBJECT_PROCESSED,
        move_object=True,
        gcp_conn_id=GCS_CONN_ID,
    )

    transform = DbtTaskGroup(
        group_id="transform",
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/']
        )

    )

    end = EmptyOperator(task_id='end')
    

# instanciate the DAG

    [begin 
    >> read_and_save_csv_str_column_task
    >> copy_from_local_to_gcs 
    >> move_files_to_processed_task 
    >> insert_gcs_to_bigquery 
    >> move_files_gcs_to_processed_gcs 
    >> transform
    >> end]

pipeline()