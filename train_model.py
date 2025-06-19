import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from joblib import dump
import json

df = pd.read_csv("simulated_data_extended.csv")

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df, columns=["Crop", "Season"])

X = df_encoded.drop(columns=["Irrigation"])
y = df_encoded["Irrigation"]

# Save the feature columns order to JSON
with open("model_features.json", "w") as f:
    json.dump(list(X.columns), f)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

dump(model, "irrigation_model_extended.joblib")
print("Model and feature list saved.")
