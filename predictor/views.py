from django.shortcuts import render
from django.http import JsonResponse
import joblib
import numpy as np
from .models import AccidentRecord

# Load the pre-trained model and preprocessing objects
model = joblib.load('predictor/files/accident_model.pkl')
scaler = joblib.load('predictor/files/scale_traffic.pkl')
label_encoders = joblib.load('predictor/files/label_encoders_traffic.pkl')

def safe_transform(encoder, value):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        # Return a default value (e.g., the first class in the encoder)
        return encoder.transform([encoder.classes_[0]])[0]  # Default to the first class

def predict_view(request):
    if request.method == 'POST':
        try:
            # Extract form data
            latitude = float(request.POST['latitude'])
            longitude = float(request.POST['longitude'])
            location = request.POST['location']
            weather_condition = request.POST['weather_condition']
            description = request.POST['description']

            # Safely transform categorical data using label encoders
            location_encoded = safe_transform(label_encoders['location'], location)
            weather_condition_encoded = safe_transform(label_encoders['weather_condition'], weather_condition)
            description_encoded = safe_transform(label_encoders['description'], description)

            # Scale numerical features
            scaled_features = scaler.transform([[latitude, longitude]])

            # Prepare input for prediction
            input_features = np.array([
                scaled_features[0][0],
                scaled_features[0][1],
                location_encoded,
                weather_condition_encoded,
                description_encoded
            ]).reshape(1, -1)

            # Predict severity
            severity = model.predict(input_features)[0]

            # Save the prediction to the database
            AccidentRecord.objects.create(
                latitude=latitude,
                longitude=longitude,
                location=location,
                weather_condition=weather_condition,
                description=description,
                severity=severity
            )

            # Render the result page
            return render(request, 'result.html', {'severity': severity})
        except Exception as e:
            # Log the error for debugging purposes (optional)
            print(f"Error: {e}")
            return render(request, 'result.html', {'error': str(e)})

    return render(request, 'predict.html')
