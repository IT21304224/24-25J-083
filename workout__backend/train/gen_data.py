import pandas as pd
import numpy as np

# Function to generate a workout plan based on logical conditions
def generate_workout_plan(weight, height, bmi, age, gender, intensity, heart_rate, blood_pressure):
    # Defining workout plans based on logic
    if blood_pressure > 140 or heart_rate > 100:  # High-risk conditions
        return "Low-Intensity Cardio or Yoga (Consult a Doctor)"
    elif bmi < 18.5:  # Underweight - focus on strength and muscle building
        return "Strength Training and Muscle Building"
    elif bmi >= 18.5 and bmi <= 24.9:  # Healthy BMI - mixed routines are ideal
        if age < 30:
            return "Mixed Routine (Cardio + Strength)" if intensity > 2 else "Strength Training and Muscle Building"
        elif age >= 30 and age < 50:
            return "Mixed Routine (Cardio + Strength)" if intensity > 2 else "Yoga and Flexibility Exercises"
        else:
            return "Yoga and Flexibility Exercises"
    elif bmi >= 25 and bmi < 30:  # Overweight - focus on cardio and fat loss
        return "Low-Impact Aerobic Exercises" if intensity < 3 else "High-Intensity Interval Training"
    else:  # Obese - focus on low-impact aerobic or cardio
        return "Low-Impact Aerobic Exercises" if intensity < 3 else "High-Intensity Interval Training"

# Generate synthetic data based on the logic
def generate_data(num_samples):
    data = []
    for _ in range(num_samples):
        weight = round(np.random.uniform(40, 120), 1)  # Weight in kg
        height = round(np.random.uniform(150, 200), 1)  # Height in cm
        bmi = round(weight / ((height / 100) ** 2), 1)  # BMI calculation
        age = np.random.randint(18, 60)  # Age between 18 and 60
        gender = np.random.choice(["Male", "Female"])  # Only Male or Female
        intensity = np.random.randint(1, 5)  # Exercise intensity scale (1-4)
        heart_rate = np.random.randint(60, 130)  # Heart rate in bpm
        blood_pressure = np.random.randint(90, 180)  # Blood pressure (systolic)
        
        # Select workout plan using logic
        plan = generate_workout_plan(weight, height, bmi, age, gender, intensity, heart_rate, blood_pressure)
        
        # Append data to list
        data.append([weight, height, bmi, age, gender, intensity, heart_rate, blood_pressure, plan])
    return data

# Generate a dataset with 500,000 samples
num_samples = 500000
columns = ["Weight", "Height", "BMI", "Age", "Gender", "Exercise Intensity", "Heart Rate", "Blood Pressure", "Workout Plan"]
dataset = generate_data(num_samples)

# Save to CSV
df = pd.DataFrame(dataset, columns=columns)
df.to_csv("dataset.csv", index=False)

print(f"Generated dataset with {num_samples} samples saved as 'workout_plans_with_health_data.csv'.")
