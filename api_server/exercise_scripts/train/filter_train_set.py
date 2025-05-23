import pandas as pd

# Load the CSV dataset into a DataFrame
df = pd.read_csv('test.csv')

# Select only the columns 'label', 'left_hip_y', and 'right_hip_y'
df_filtered = df[['label', 'left_hip_y', 'right_hip_y']]

# Optionally, save the filtered DataFrame to a new CSV file
df_filtered.to_csv('test2.csv', index=False)

# Display the filtered DataFrame
print(df_filtered.head())
