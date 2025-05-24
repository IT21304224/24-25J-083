import pandas as pd
import joblib

# Load the trained model, scaler, and label encoders
model = joblib.load('train/model/workout_model.pkl')
scaler = joblib.load('train/model/scaler.pkl')
label_encoder_gender = joblib.load('train/model/label_encoder_gender.pkl')
label_encoder_workout_plan = joblib.load('train/model/label_encoder_workout_plan.pkl')

# Input new data for prediction (including all relevant features)
new_data = pd.DataFrame({
    'Weight': [600],               # Weight in kg
    'Height': [175],              # Height in cm
    'BMI': [30.0],                # BMI (pre-calculated or can be recalculated dynamically)
    'Age': [22],                  # Age in years
    'Gender': ['Female'],         # Gender as a string (will be encoded)
    'Exercise Intensity': [4],    # Intensity scale (1-4)
    'Heart Rate': [80],           # Heart rate in bpm
    'Blood Pressure': [120]       # Systolic blood pressure
})

# Transform categorical features using the saved label encoders
new_data['Gender'] = label_encoder_gender.transform(new_data['Gender'])

# Scale the new data using the saved scaler
new_data_scaled = scaler.transform(new_data)

# Predict the workout plan using the trained model
new_prediction = model.predict(new_data_scaled)

# Decode the predicted workout plan back to the original label
predicted_workout_plan = label_encoder_workout_plan.inverse_transform(new_prediction)

# Print the result
print(f'Predicted Workout Plan: {predicted_workout_plan[0]}')
