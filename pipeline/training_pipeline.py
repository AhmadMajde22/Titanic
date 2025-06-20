from src.data_ingestion import DataIngestion
from config.database_config import *
from config.path_config import *
from src.feature_store import RedisFeatureStore
from src.data_processing import DataProcessing
from src.model_training import ModelTraining


if __name__ == "__main__":
    data_ingestion = DataIngestion(DB_CONFIG,RAW_DIR)
    data_ingestion.run()

    feature_store = RedisFeatureStore()
    data_processor = DataProcessing(
        train_data_path=TRAIN_PATH,
        test_data_path=TEST_PATH,
        feature_store=feature_store)
    data_processor.run()


    feature_store = RedisFeatureStore()
    model_training = ModelTraining(feature_store,MODEL_SAVE_PATH)

    model_training.run()
