# Data Pipeline Project with Airflow, dbt, and Google Cloud

## Overview
### This project involves building an automated data pipeline using Airflow, Cosmos, dbt, and Google Cloud. The main goal of this pipeline is to integrate different data sources, process and transform raw data, and store it in a cloud data warehouse (Google BigQuery). The project uses Docker for containerization and orchestration to ensure easy deployment and scalability. Below is a step-by-step breakdown of how the data pipeline is built and operates. ⬇️⬇️!

## Architecture:
![Pipeline](assets/project_arch)

## Building the Pipeline
================
1. Data Ingestion: Store raw data in a scalable data lake. Here we'll use Google cloud storage (GCS).

2. ETL/ELT Pipelines:
    - Move data from the lake to a structured data warehouse, BigQuery.
    - Use dbt (dbt cli) to define simple models for transforming raw data into meaningful, analytics-ready models.

3. Orchestration: Use Airflow (via Astronomer) to automate and schedule pipeline tasks.

1. [Docker](https://www.docker.com):
    Docker is a containerization platform that allows you to package applications and their dependencies into portable containers. In this project, Docker is used to containerize all components of the pipeline (dbt, Airflow, Metabase,     etc.), ensuring consistent environments across local development and deployment. It simplifies setup and makes the pipeline reproducible and scalable.

2. [Astro](https://www.astronomer.io/docs):
    Astro (by Astronomer) is a cloud-native data orchestration platform built around Apache Airflow. It simplifies Airflow deployment, monitoring, and scaling. In this project, Astro is used to deploy and manage Airflow pipelines with     a production-grade interface, providing version control, observability, and seamless integration with tools like Cosmos and dbt.

3. [Airflow](https://airflow.apache.org):
    Apache Airflow is an open-source workflow orchestration tool used to programmatically create, schedule, and monitor data workflows. In this project, Airflow is used to automate the ETL process — from ingesting raw data to GCS,         uploading to BigQuery, transforming with dbt, to quality testing — enabling full reliable pipeline automation.

5. [Google Cloud Storage (GCS)](https://console.cloud.google.com):
GCS is an object storage service for unstructured data. It serves as the data lake in this project, where raw Billboard datasets are initially stored. GCS provides scalable, cost-effective storage that can be accessed by Airflow       and dbt for downstream processing.

6. [BigQuery](https://console.cloud.google.com):
    BigQuery is a fully managed, serverless data warehouse by Google Cloud. In this project, it acts as the central data warehouse, where cleaned and transformed data (via dbt) is loaded. It enables fast, SQL-based analysis and            supports seamless integration with BI tools like Metabase for reporting.

8. [DBT](https://www.getdbt.com/):
    dbt (data build tool) is used for transforming raw data in the warehouse using SQL and modular, version-controlled data models. In this project, dbt is used to transform data and make them data analysis-ready in BigQuery. The CLI      version is used and it allows tight integration with Airflow and Cosmos for automation.

9. [Cosmos](https://www.astronomer.io/cosmos):
    Cosmos is an open-source Airflow provider by Astronomer that allows you to run dbt projects natively as Airflow tasks. In this project, Cosmos dynamically converts dbt models into Airflow tasks with their dependencies preserved,       enabling fine-grained orchestration, monitoring, and retries — all while keeping the dbt DAG structure intact.


Contact
=======
Connect with me on LinkedIn ✌️ : [Guilherme Arruda](https://www.linkedin.com/in/arruda-guilherme/)