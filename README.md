# Titanic Survival Prediction MLOps Project

## Overview

This project implements an end-to-end MLOps pipeline for predicting Titanic passenger survival. It covers data ingestion, processing, feature engineering, model training, evaluation, and deployment using modern MLOps practices. The project leverages Airflow for orchestration, Docker for containerization, and follows best practices for reproducibility and automation.

## Project Structure

```
├── artifacts/                # Data and model artifacts
│   ├── models/               # Trained models
│   └── raw/                  # Raw datasets
├── astro_project/            # Airflow project (DAGs, configs, Dockerfile)
│   ├── dags/                 # Airflow DAGs
│   ├── airflow_settings.yaml # Airflow settings
│   ├── Dockerfile            # Airflow Dockerfile
│   └── requirements.txt      # Airflow requirements
├── config/                   # Configuration files
├── logs/                     # Log files
├── notebook/                 # Jupyter notebooks for EDA and prototyping
├── pipeline/                 # Pipeline scripts
├── src/                      # Source code (data, features, model, utils)
├── tests/                    # Unit and integration tests
├── requirements.txt          # Project dependencies
├── setup.py                  # Package setup
└── README.md                 # Project documentation
```

## Features

- **Data Ingestion:** Automated download and management of Titanic datasets from MinIO using Airflow.
- **Data Processing:** Cleaning, feature engineering, and storage in PostgreSQL.
- **Model Training:** Random Forest classifier with hyperparameter tuning.
- **Orchestration:** Airflow DAGs for pipeline automation.
- **Containerization:** Docker support for reproducible environments.
- **Testing:** Unit and integration tests for pipeline components.
- **Logging:** Centralized logging for monitoring and debugging.

## Data Ingestion and Storage

### How Data Ingestion Works

- Data ingestion is managed by an Airflow DAG located in `astro_project/dags/download_titanic_from_minio.py`.
- The DAG connects to a MinIO bucket, downloads the Titanic dataset (CSV files), and stores them in the `artifacts/raw/` directory.
- After downloading, the data is ingested into a PostgreSQL database for further processing and analysis.

### Steps to Ingest Data from MinIO and Store in PostgreSQL

1. **Start Airflow:**
   - Use the provided Dockerfile and Airflow setup in `astro_project/` to start Airflow.
   - Make sure your MinIO and PostgreSQL services are running and accessible.

2. **Configure Connections:**
   - In the Airflow UI, set up connections for MinIO (S3-compatible) and PostgreSQL with the correct credentials.

3. **Trigger the DAG:**
   - In the Airflow UI, trigger the `download_titanic_from_minio` DAG.
   - The DAG will:
     - Connect to MinIO and download the Titanic dataset.
     - Store the raw data in `artifacts/raw/`.
     - Load the data into the configured PostgreSQL database.

4. **Verify Data:**
   - Check the `artifacts/raw/` directory for downloaded files.
   - Verify that the data has been loaded into the PostgreSQL database (e.g., using a database client).

## Notebooks

- Explore `notebook/notebook.ipynb` for EDA, feature exploration, and model prototyping.

## Configuration

- All configuration files are in the `config/` directory.
- Update `config/database_config.py` and `config/path_config.py` as needed.
