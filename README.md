# Titanic Survival Prediction MLOps Project

## Overview

This project implements an end-to-end MLOps pipeline for predicting Titanic passenger survival. It covers data ingestion, processing, feature engineering, model training, evaluation, and deployment using modern MLOps practices. The project leverages Airflow for orchestration, Docker for containerization, and follows best practices for reproducibility and automation.

## Project Structure

```text
├── artifacts/                # Data and model artifacts
│   ├── models/               # Trained models (e.g., random_forest_model.pkl)
│   └── raw/                  # Raw datasets (titanic_train.csv, titanic_test.csv)
├── astro_project/            # Airflow project for orchestration
│   ├── dags/                 # Airflow DAGs (e.g., download_titanic_from_minio.py)
│   ├── airflow_settings.yaml # Airflow settings for local development
│   ├── Dockerfile            # Dockerfile for Airflow environment
│   ├── packages.txt          # OS-level packages for Airflow
│   ├── plugins/              # Custom Airflow plugins
│   ├── include/              # Additional files for Airflow
│   ├── requirements.txt      # Python dependencies for Airflow
│   └── tests/                # Airflow DAG tests
├── config/                   # Project configuration files
│   ├── __init__.py
│   ├── database_config.py    # Database connection settings
│   └── path_config.py        # Path and directory settings
├── docker-compose.yml        # Docker Compose file for Prometheus & Grafana monitoring stack
├── logs/                     # Log files for pipeline and app
├── notebook/                 # Jupyter notebooks for EDA and prototyping
│   └── notebook.ipynb
├── pipeline/                 # Pipeline scripts
│   ├── __init__.py
│   └── training_pipeline.py  # Main training pipeline script
├── prometheus.yml            # Prometheus configuration for scraping metrics
├── src/                      # Source code (data, features, model, utils)
│   ├── __init__.py
│   ├── custom_exception.py   # Custom exception handling
│   ├── data_ingestion.py     # Data ingestion logic
│   ├── data_processing.py    # Data processing and drift detection
│   ├── feature_store.py      # Feature store integration (e.g., Redis)
│   ├── logger.py             # Logging utility
│   └── model_training.py     # Model training logic
├── static/                   # Static files for web app (CSS, images)
│   ├── background.png
│   └── style.css
├── templates/                # HTML templates for web app
│   └── index.html
├── tests/                    # Unit and integration tests
│   └── dags/                 # Airflow DAG tests
│       ├── download_titanic_from_minio.py
│       └── test_dag_example.py
├── requirements.txt          # Project dependencies for main app
├── setup.py                  # Python package setup
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

## Data Drift

- **Detection:** The application uses the Kolmogorov-Smirnov (KS) test via the `alibi-detect` library to monitor and detect data drift between the training data and new incoming data.
- **Implementation:**
  - Reference (historical) feature data is loaded from a Redis feature store and scaled using `StandardScaler`.
  - For each prediction request, the input features are scaled and compared to the reference data using the KSDrift detector.
  - If drift is detected, a warning is logged.
- **Customization:**
  - You can adjust drift detection thresholds (e.g., `p_val`) and monitored features in `application.py`.
  - The reference data and scaling logic can be modified in the `fit_scaler_on_ref_data` function.
- **Dependencies:** Requires `alibi-detect`, `scikit-learn`, and a running Redis instance for the feature store.

## Web Application

- **Flask Web App:** A user-friendly web interface is provided for Titanic survival prediction.
- **Location:** The main app is in `application.py`.
- **How it works:**
  - Users input passenger features (age, fare, class, sex, etc.) via a form.
  - The app loads a trained Random Forest model (`artifacts/models/random_forest_model.pkl`).
  - On form submission, the app predicts survival and displays the result.
- **Frontend:** The interface uses `templates/index.html` and custom styles in `static/style.css`.
- **How to run:**
  1. Install requirements: `pip install -r requirements.txt`
  2. Run the app: `python application.py`
  3. Open your browser at `http://localhost:5000`
- **Customization:** You can update the look and feel via `static/style.css` and the form fields in `templates/index.html`.

## Monitoring with Prometheus and Grafana

- **Monitoring Stack:** The project includes Prometheus and Grafana for monitoring and visualization.
- **Setup:** Services are orchestrated using Docker Compose (`docker-compose.yml`).
- **Configuration:**
  - Prometheus is configured via `prometheus.yml` to scrape metrics from the Flask app.
  - Grafana is available for dashboarding and visualization.
- **How to run:**
  1. Make sure Docker is installed and running.
  2. Start the monitoring stack with:

     ```
     docker-compose up -d
     ```

  3. Access Prometheus at [http://localhost:9999](http://localhost:9999) and Grafana at [http://localhost:3333](http://localhost:3333) (default admin password: `admin`).
- **Customization:** Update `prometheus.yml` and Grafana dashboards as needed for your metrics and visualization requirements.
