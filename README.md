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

- **Data Ingestion:** Automated download and management of Titanic datasets.
- **Data Processing:** Cleaning, feature engineering, and storage.
- **Model Training:** Random Forest classifier with hyperparameter tuning.
- **Orchestration:** Airflow DAGs for pipeline automation.
- **Containerization:** Docker support for reproducible environments.
- **Testing:** Unit and integration tests for pipeline components.
- **Logging:** Centralized logging for monitoring and debugging.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker
- Apache Airflow (or use provided Docker setup)
- (Optional) Jupyter Notebook

### Installation

1. Clone the repository:

   ```sh
   git clone <repo-url>
   cd Section_3_Titanic_Survaivl_prediction/Content
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. (Optional) Set up Airflow:
   - Use the provided Dockerfile and `astro_project/` for Airflow setup.

### Running the Pipeline

- **Via Airflow:**
  1. Start Airflow (see `astro_project/README.md` for details).
  2. Trigger the DAG `download_titanic_from_minio` or other available DAGs.
- **Manual Execution:**

  ```sh
  python -m pipeline.training_pipeline
  ```

### Notebooks

- Explore `notebook/notebook.ipynb` for EDA, feature exploration, and model prototyping.

## Configuration

- All configuration files are in the `config/` directory.
- Update `config/database_config.py` and `config/path_config.py` as needed.

## Testing

- Run tests using:

  ```sh
  pytest tests/
  ```

## Logging

- Logs are stored in the `logs/` directory.

## Security & Secrets

- Sensitive files (e.g., `.env`, `config/database_config.py`) are excluded via `.gitignore`.
- Do not commit secrets or credentials to the repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License

This project is for educational purposes. See LICENSE file if available.

## Authors

- [Your Name]

## Acknowledgements

- Kaggle Titanic Dataset
- Udemy MLOps Course
- Open-source contributors
