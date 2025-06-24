import pickle

import numpy as np
import pandas as pd
from alibi_detect.cd import KSDrift
from flask import Flask, jsonify, render_template, request
from sklearn.preprocessing import StandardScaler


from src.feature_store import RedisFeatureStore
from src.logger import get_logger

from prometheus_client import start_http_server,Counter,Gauge


logger = get_logger(__name__)

app = Flask(__name__)

prediction_count = Counter("prediction_count","Number of prediction count")
drift_count =  Counter("drift_count","Number of times data drift is detected")



MODEL_PATH = r'artifacts/models/random_forest_model.pkl'

with open(MODEL_PATH,'rb') as model_file:
    model = pickle.load(model_file)

FEATURE_NAMES = ['Age', 'Fare', 'Pclass', 'Sex', 'Embarked', 'FamilySize', 'IsAlone','HasCabin', 'Title', 'Pclass_Fare', 'Age_Fare']


feature_store = RedisFeatureStore()
scaler = StandardScaler()

def fit_scaler_on_ref_data():
    entity_ids = feature_store.get_all_entity_ids()
    all_features = feature_store.get_batch_features(entity_ids)

    all_features_df = pd.DataFrame.from_dict(all_features, orient='index', columns=FEATURE_NAMES)

    scaler.fit(all_features_df)

    return scaler.transform(all_features_df)

historical_data = fit_scaler_on_ref_data()
ksd = KSDrift(x_ref = historical_data,p_val =0.05)


    

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict', methods=["POST"])
def predict():
    try:
        data = request.form
        Age = float(data['Age'])
        Fare = float(data["Fare"])
        Pclass = int(data["Pclass"])
        Sex = int(data["Sex"])
        Embarked = int(data["Embarked"])
        FamilySize = int(data["FamilySize"])
        IsAlone = int(data["IsAlone"])
        HasCabin = int(data["HasCabin"])
        Title = int(data["Title"])
        Pclass_Fare = float(data['Pclass_Fare'])
        Age_Fare = float(data["Age_Fare"])

        features = pd.DataFrame([[Age,Fare,Pclass,Sex,Embarked,FamilySize,IsAlone,HasCabin,Title,Pclass_Fare,Age_Fare]],columns=FEATURE_NAMES)

        features_scaled = scaler.transform(features)

        drift = ksd.predict(features_scaled)

        drift_response = drift.get('data', {})
        is_drift = drift_response.get('is_drift', None)

        if is_drift is not None and is_drift:
            print("Drift detected in the input features.")
            logger.warning("Drift detected in the input features.")

            drift_count.inc()

        prediction = model.predict(features)[0]

        prediction_count.inc()

        result = "Survived" if prediction == 1 else "Didn't Survive"

        return render_template("index.html", prediction=result)
    except Exception as e:
        return jsonify("index.html", prediction=f"Error: {str(e)}")


@app.route("/metrics")
def metrics():
    from prometheus_client import generate_latest

    from flask import Response

    return Response(generate_latest(),content_type="text/plain")

if __name__ == "__main__":
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_http_server(7010)
    app.run(debug=True, host='0.0.0.0', port=5000)
