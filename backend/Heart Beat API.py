from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import joblib
import os

app = Flask(__name__)
CORS(app)

# load model and scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/heart_disease_model.keras')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '../scaler/scaler.save')

model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # expecting a list of features in the correct order
    features = np.array([data['features']])
    features_scaled = scaler.transform(features)
    risk = model.predict(features_scaled)
    risk_percent = float(risk[0][0]) * 100
    return jsonify({
        'risk_percent': round(risk_percent, 2),
        'risk_level': 'High' if risk_percent > 50 else 'Low'
    })

if __name__ == '__main__':
    app.run(debug=True)
