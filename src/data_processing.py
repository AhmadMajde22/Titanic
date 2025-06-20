import sys

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

from config.path_config import *
from src.custom_exception import CustomException
from src.feature_store import RedisFeatureStore
from src.logger import get_logger

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self,train_data_path,test_data_path,feature_store : RedisFeatureStore):
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.data = None
        self.test_data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.X_resampled = None
        self.y_resampled = None

        self.feature_store = feature_store

        logger.info("Data Processing Initinalized....")

    def load_data(self):
        try:
            self.data = pd.read_csv(self.train_data_path)
            self.test_data = pd.read_csv(self.test_data_path)
            logger.info("Reading Data Sucessfully...")
        except Exception as e:
            logger.error(f"Error While reading data {e}")
            raise CustomException(str(e),sys)

    def preprocess_data(self):
        try:
            self.data['Age'] = self.data['Age'].fillna(self.data['Age'].median())
            self.test_data['Age'] = self.test_data['Age'].fillna(self.test_data['Age'].median())

            self.data['Embarked'] = self.data['Embarked'].fillna(self.data['Embarked'].mode()[0])
            self.test_data['Embarked'] = self.test_data['Embarked'].fillna(self.test_data['Embarked'].mode()[0])

            self.data['Fare'] = self.data['Fare'].fillna(self.data['Fare'].median())
            self.test_data['Fare'] = self.test_data['Fare'].fillna(self.test_data['Fare'].median())

            self.data["Sex"] = self.data['Sex'].map({'male':0,"female":1})
            self.test_data["Sex"] = self.test_data['Sex'].map({'male':0,"female":1})

            self.data['Embarked'] = self.data['Embarked'].astype('category').cat.codes
            self.test_data['Embarked'] = self.test_data['Embarked'].astype('category').cat.codes


            self.data['FamilySize'] = self.data['SibSp'] + self.data["Parch"] + 1
            self.test_data['FamilySize'] = self.test_data['SibSp'] + self.test_data["Parch"] + 1


            self.data["IsAlone"] = (self.data["FamilySize"] == 1).astype(int)
            self.test_data["IsAlone"] = (self.test_data["FamilySize"] == 1).astype(int)


            self.data["HasCabin"] = self.data["Cabin"].notnull().astype(int)
            self.test_data["HasCabin"] = self.test_data["Cabin"].notnull().astype(int)


            self.data["Title"] = self.data['Name'].str.extract(' ([A-Za-z]+)\.',expand=False).map({
                    "Mr":0,"Miss":1,"Mrs":2,"Master":3,"Rare":4}).fillna(4)

            self.test_data["Title"] = self.test_data['Name'].str.extract(' ([A-Za-z]+)\.',expand=False).map({
                    "Mr":0,"Miss":1,"Mrs":2,"Master":3,"Rare":4}).fillna(4)

            self.data["Pclass_Fare"] = self.data['Pclass'] * self.data["Fare"]
            self.test_data["Pclass_Fare"] = self.test_data['Pclass'] * self.test_data["Fare"]


            self.data["Age_Fare"] = self.data["Age"] * self.data["Fare"]
            self.test_data["Age_Fare"] = self.test_data["Age"] * self.test_data["Fare"]

            logger.info(f"Data Preprocessing Done....")
        except Exception as e:
            logger.error("Error While Preprocessing data",e)
            raise CustomException(str(e),sys)


    def split_handle_imbalance_data(self):
        try:
            self.X_train = self.data[["Pclass","Sex","Age","Fare","Embarked","FamilySize","IsAlone","HasCabin","Title","Pclass_Fare","Age_Fare"]]
            self.X_test = self.test_data[["Pclass","Sex","Age","Fare","Embarked","FamilySize","IsAlone","HasCabin","Title","Pclass_Fare","Age_Fare"]]

            self.y_train = self.data["Survived"]
            self.y_test = self.test_data["Survived"]


            smote= SMOTE(random_state=42)
            self.X_resampled , self.y_resampled = smote.fit_resample(self.X_train,self.y_train)

            logger.info("Handle Imbalance data Sucessfully...")

        except Exception as e:
            logger.error("Error While Handle Imbalance data",e)
            raise CustomException(str(e),sys)


    def store_fetures_in_redis(self):
        try:
            batch_data = {}
            for idx ,row in self.data.iterrows():
                entity_id =row["PassengerId"]
                features = {
                    "Age":row['Age'],
                    "Fare":row["Fare"],
                    "Pclass":row["Pclass"],
                    "Sex" : row["Sex"],
                    "Embarked":row["Embarked"],
                    "FamilySize": row["FamilySize"],
                    "IsAlone":row["IsAlone"],
                    "HasCabin":row["HasCabin"],
                    "Title":row["Title"],
                    "Pclass_Fare":row["Pclass_Fare"],
                    "Age_Fare":row["Age_Fare"],
                    "Survived" : row["Survived"]
                }
                batch_data[entity_id] =features
            self.feature_store.store_batch_features(batch_data)
            logger.info("Data has been feeded into Feature Store (Redis)...")

        except Exception as e:
            logger.error("Error While Fedding data into Features store",e)
            raise CustomException(str(e),sys)


    def retrive_feature_redis_store(self,entity_id):
        features = self.feature_store.get_features(entity_id)
        if features:
            return features
        return None

    def run(self):
        try:
            logger.info("Starting Our Data Processing Pipeline .....")
            self.load_data()
            self.preprocess_data()
            self.split_handle_imbalance_data()
            self.store_fetures_in_redis()

            logger.info("End Of Preprocessing Data Pipeline")

        except Exception as e:
            logger.error("Error While Running the Data Preprocessing Pipeline",e)
            raise CustomException(str(e),sys)
            


if __name__ == "__main__":
    feature_store = RedisFeatureStore()
    data_processor = DataProcessing(
        train_data_path=TRAIN_PATH,
        test_data_path=TEST_PATH,
        feature_store=feature_store
    )
    data_processor.run()

    # print(data_processor.retrive_feature_redis_store(entity_id=332))
    
