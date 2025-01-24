import pickle
import pandas as pd
from django.shortcuts import render

# Load the model and preprocessors
with open('predictor/files/kmeans_model(1).pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

with open('predictor/files/scaler(1).pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('predictor/files/label_encoder_weather.pkl', 'rb') as le_weather_file:
    label_encoder_weather = pickle.load(le_weather_file)

with open('predictor/files/label_encoder_lighting.pkl', 'rb') as le_lighting_file:
    label_encoder_lighting = pickle.load(le_lighting_file)

def predict_hotspot(request):
    cluster = None
    latitude = None
    longitude = None

    if request.method == "POST":
        try:
            # Collect user input
            input_data = {
                'Latitude': float(request.POST.get('latitude')),
                'Longitude': float(request.POST.get('longitude')),
                'Traffic_Volume': float(request.POST.get('traffic_volume')),
                'Speed_Limit': float(request.POST.get('speed_limit')),
                'Visibility': float(request.POST.get('visibility')),
                'Weather_Condition': request.POST.get('weather_condition'),
                'Lighting_Condition': request.POST.get('lighting_condition'),
            }

            # Encode categorical variables
            input_data['Weather_Condition'] = label_encoder_weather.transform([input_data['Weather_Condition']])[0]
            input_data['Lighting_Condition'] = label_encoder_lighting.transform([input_data['Lighting_Condition']])[0]

            # Convert to DataFrame
            input_df = pd.DataFrame([input_data])

            # Select features for scaling
            features = ['Latitude', 'Longitude', 'Traffic_Volume', 'Speed_Limit', 'Visibility']
            input_df_scaled = input_df.copy()
            input_df_scaled[features] = scaler.transform(input_df[features])

            # Predict the cluster
            cluster = kmeans.predict(input_df_scaled[features])[0]

            # Store latitude and longitude for mapping
            latitude = input_data['Latitude']
            longitude = input_data['Longitude']

        except Exception as e:
            print(f"Error: {e}")
            cluster = "Error in processing the input data"

    return render(request, "traffic_hotspots.html", {
        "cluster": cluster,
        "latitude": latitude,
        "longitude": longitude
    })
