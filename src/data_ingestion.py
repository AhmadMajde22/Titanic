import os
import sys

import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split

from config.database_config import DB_CONFIG
from config.path_config import *
from config.path_config import RAW_DIR, TEST_PATH, TRAIN_PATH
from src.custom_exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)

class DataIngestion:

    def  __init__(self,db_params,output_dir):
        self.db_params = db_params
        self.output_dir = output_dir

        os.makedirs(self.output_dir,exist_ok=True)


    def connect_db(self):
        try:
            conn = psycopg2.connect(
                host = self.db_params['host'],
                port = self.db_params['port'],
                dbname = self.db_params['db_name'],
                user = self.db_params['user'],
                password = self.db_params['password']
            )

            logger.info("Database connection established ...")
            return conn
        except Exception as e:
            logger.error("Error While esatblishing connection ",e)
            raise CustomException(str(e),sys)

    def extract_data(self):
        try:
            conn = self.connect_db()
            query = "SELECT * FROM public.titanic_dataset"
            df = pd.read_sql_query(query,conn)
            conn.close()
            logger.info("Data Extracted FROM DB Sucessfully...")
            return df
        except Exception as e:
            logger.error("Error While extracting dataset ",e)
            raise CustomException(str(e),sys)

    def save_data(self,df):
        try:
            train_df , test_df = train_test_split(df,test_size=0.2,random_state=42)
            train_df.to_csv(TRAIN_PATH,index=False)
            test_df.to_csv(TEST_PATH,index=False)

            logger.info("Data Splitting and Saving Done...")

        except Exception as e:
            logger.error("Error While Saveing dataset ",e)
            raise CustomException(str(e),sys)

    def run(self):
        try:
            logger.info("Data Ingestion Pipeline started...")
            df = self.extract_data()
            self.save_data(df)

            logger.info("End Of Data Ingestion Pipeline....")

        except Exception as e:
            logger.error("Error While Data Ingestion Pipeline ",e)
            raise CustomException(str(e),sys)


if __name__ == "__main__":
    data_ingestion = DataIngestion(DB_CONFIG,RAW_DIR)
    data_ingestion.run()
