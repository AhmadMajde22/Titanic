import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

from config.path_config import *
from src.custom_exception import CustomException
from src.feature_store import RedisFeatureStore
from src.logger import get_logger


logger = get_logger(__name__)

class ModelTraining:
    def __init__(self,feature_store:RedisFeatureStore,model_save_path):
        self.feature_store = feature_store
        self.model_save_path = model_save_path
        self.model = None 

        os.makedirs(self.model_save_path,exist_ok=True)
        logger.info("Model Training Initialized.....")


    def load_data_from_redis(self,entity_ids):
        try:
            logger.info("Extracting Data from redis")

            data = []
            for entity_id in entity_ids:
                features = self.feature_store.get_features(entity_id)
                if features:
                    data.append(features)
                else:
                    logger.warning(f"There Is No Features in {entity_id}")

            return data 

        except Exception as e :
            logger.error("Error While Loading Data From Redis ",e)
            raise CustomException(str(e),sys)


    def prepare_data(self):
        try:
            entity_ids = self.feature_store.get_all_entity_ids()

            train_entity_ids , test_entity_ids = train_test_split(entity_ids,test_size=0.2,random_state=42)

            train_data = self.load_data_from_redis(train_entity_ids)

            test_data = self.load_data_from_redis(test_entity_ids)

            train_df = pd.DataFrame(train_data)

            test_df = pd.DataFrame(test_data)

            X_train = train_df.drop("Survived",axis=1)
            logger.info(X_train.columns)

            X_test = test_df.drop("Survived",axis=1)

            y_train = train_df["Survived"]
            y_test = test_df["Survived"]

            logger.info("Data Preperation Is Done....")
            
            return X_train,X_test,y_train,y_test

        except Exception as e :
            logger.error("Error While Prepare Data ",e)
            raise CustomException(str(e),sys)

    def hyperparamter_tuning(self,X_train,y_train):
        try:
            param_distributions = {
                "n_estimators": [100,200,300],
                "max_depth" : [10,20,30],
                "min_samples_split" : [2,5],
                "min_samples_leaf":[1,2]
            }
            rf = RandomForestClassifier(random_state=42)
            random_search = RandomizedSearchCV(
            rf,param_distributions,n_iter=10,cv=3,scoring='accuracy',random_state=42)
            random_search.fit(X_train,y_train)

            logger.info(f"Best Parameters {random_search.best_params_}")

            return random_search.best_estimator_

        except Exception as e :
            logger.error("Error While hyperparamter tuning ",e)
            raise CustomException(str(e),sys)


    def train_and_evaluate(self,X_train,y_train,X_test,y_test):
        try:
            best_rf = self.hyperparamter_tuning(X_train,y_train)

            y_pred = best_rf.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)

            logger.info(f"Accuracy is {accuracy}")

            self.save_model(best_rf)

            return accuracy

        except Exception as e :
            logger.error("Error While evaluate the Model",e)
            raise CustomException(str(e),sys) 

    def save_model(self,model):
        try:
            model_filename = f"{self.model_save_path}random_forest_model.pkl"

            with open(model_filename,"wb") as model_file:
                pickle.dump(model,model_file)

            logger.info(f"Model Saved at{model_filename}")

        except Exception as e :
            logger.error("Error While Saving the Model",e)
            raise CustomException(str(e),sys) 

    def run(self):
        try:
            logger.info("Starting Model Training Pipeline")

            X_train,X_test,y_train,y_test = self.prepare_data()

            accuracy = self.train_and_evaluate(X_train,y_train,X_test,y_test)

            logger.info(f"End Of Model Training Pipeline with {accuracy:.2f}% accuracy")


        except Exception as e :
            logger.error("Error While Training the Model Pipeline",e)
            raise CustomException(str(e),sys) 

            

if __name__=="__main__":
    feature_store = RedisFeatureStore()
    model_training = ModelTraining(feature_store,MODEL_SAVE_PATH)

    model_training.run()
            


    