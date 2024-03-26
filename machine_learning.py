import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, make_scorer, classification_report

import xgboost as xgb

# Import the DataFrame from the CSV file
df = pd.read_csv('dataset.csv')

## Check missing values
missing_values = df.isnull().sum()

## Drop the rows whose tmin and tmax is NaN.
df.dropna(subset=['tmin', 'tmax'], inplace=True)

## Drop the rows whose elevation_result is NaN
df.dropna(subset=['elevation_result'], inplace=True)

## Drop the rows whose cropland is NaN
df.dropna(subset=['cropland'], inplace=True)

print(f"df: {df.shape}")

# Drop rows where crop is shrubs and desrt
cropland_to_drop = [152, 141, 142, 143]

df_shrubs = df[df['cropland'].isin(cropland_to_drop)]
df = df[~df['cropland'].isin(cropland_to_drop)]

print(f"df_shrubs: {df_shrubs.shape}")
print(f"df: {df.shape}")

plt.figure(figsize=(8, 6))
plt.hist(df['cropland'], bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of Column: ' + 'cropland' + ' of df_shrubs')
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

accuracies_df = pd.DataFrame(columns=["model", "irrigation", "cropland"])

def add_accuracy(model, accuracy_irrigation, accuracy_cropland):
    global accuracies_df
    # Append the accuracy data to the DataFrame
    new_data = pd.DataFrame({
        "model": [model],
        "irrigation": [accuracy_irrigation],
        "cropland": [accuracy_cropland]
    })
    # Concatenate the new DataFrame with the existing one
    accuracies_df = pd.concat([accuracies_df, new_data], ignore_index=True)

    X = df[['lat', 'lon', 'tmin', 'tmax', 'prcp', 'elevation_result']]  # Features
y_irrigation = df['irrigation_result']  # Target 1
y_cropland = df['cropland']  # Target 2

le_irrigation = LabelEncoder()
le_cropland = LabelEncoder()

y_irrigation_encoded = le_irrigation.fit_transform(df['irrigation_result'])
y_cropland_encoded = le_cropland.fit_transform(df['cropland'])

# Now split the data with the encoded targets
X_train, X_test, y_irrigation_train, y_irrigation_test = train_test_split(
    X, y_irrigation_encoded, test_size=0.2, random_state=42
)
X_train, X_test, y_cropland_train, y_cropland_test = train_test_split(
    X, y_cropland_encoded, test_size=0.2, random_state=42
)


# Model for irrigation_result
model_irrigation = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model_irrigation.fit(X_train, y_irrigation_train)

# Model for cropland
model_cropland = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
model_cropland.fit(X_train, y_cropland_train)

# Predictions
y_irrigation_pred = model_irrigation.predict(X_test)
y_cropland_pred = model_cropland.predict(X_test)

# Accuracy
accuracy_irrigation = accuracy_score(y_irrigation_test, y_irrigation_pred)
accuracy_cropland = accuracy_score(y_cropland_test, y_cropland_pred)

# Save the accuracies
add_accuracy("xgboost", accuracy_irrigation, accuracy_cropland)

print(f"Accuracy for Irrigation Result: {accuracy_irrigation}")
print(f"Accuracy for Cropland: {accuracy_cropland}")
