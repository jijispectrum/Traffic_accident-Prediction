import pickle
import pandas as pd
from django.shortcuts import render
from .models import TrafficData
from sklearn.preprocessing import StandardScaler,LabelEncoder

# Load the trained KMeans model and scaler from pickle files
with open('predictor/files/kmeans_model.pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

with open('predictor/files/kmeans_scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def predict_hotspot(request):
    # Example input data for prediction (you can get this from user input or database)
    input_data = {
        'Latitude': 10.8505,
        'Longitude': 76.2711,
        'Traffic_Volume': 1200,
        'Speed_Limit': 50,
        'Visibility': 1000,
        'Weather_condition':3,
        'Lighting_Condition':

    }

    # Convert input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data (scaling)
    scaled_input = scaler.transform(input_df)

    # Predict the cluster (hotspot)
    cluster = kmeans.predict(scaled_input)

    # Render the result on a webpage
    return render(request, "traffic_hotspot_result.html", {"cluster": cluster[1]})