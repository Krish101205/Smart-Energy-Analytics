"""
train_model.py
---------------
Retrains the ML model on the NEW dataset with per-appliance daily hours.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ============================================================
# 1. Load the dataset
# ============================================================
df = pd.read_csv("data/raw/electricity_bill_dataset_v2.csv")
print("Loaded dataset:", df.shape)

# ============================================================
# 2. Encode the City column
# ============================================================
city_encoder = LabelEncoder()
df["CityEncoded"] = city_encoder.fit_transform(df["City"])

# ============================================================
# 3. Define input features (X) and target (y)
# ============================================================
feature_columns = [
    "Fan", "FanHours",
    "Refrigerator", "RefrigeratorHours",
    "AirConditioner", "AirConditionerHours",
    "Television", "TelevisionHours",
    "Monitor", "MonitorHours",
    "MotorPump", "MotorPumpHours",
    "Month", "CityEncoded",
]
X = df[feature_columns]
y = df["ElectricityBill"]

# ============================================================
# 4. Split into train/test sets
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# 5. Train the model
# ============================================================
model = RandomForestRegressor(
    n_estimators=100,       # fewer trees (still plenty)
    max_depth=12,           # limits how deep each tree grows
    min_samples_leaf=5,     # avoids overly specific tiny leaves
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)

# ============================================================
# 6. Check accuracy
# ============================================================
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Train R² score: {train_score:.4f}")
print(f"Test R² score: {test_score:.4f}")

# ============================================================
# 7. Save the model + encoder
# ============================================================
joblib.dump(model, "models/electricity_bill_model_v2.pkl", compress=3)
joblib.dump(city_encoder, "models/city_encoder_v2.pkl", compress=3)
print("\n✅ Saved new model to models/electricity_bill_model_v2.pkl")
