# Save this as trainer.py and run it once
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

def train_model():
    df = pd.read_csv("data/creditcard.csv")
    
    # Create Behavioral Feature
    df['UserID'] = df.index % 1000
    df['avg_amount'] = df.groupby('UserID')['Amount'].transform('mean')
    df['deviation'] = df['Amount'] / (df['avg_amount'] + 1)
    
    scaler = StandardScaler()
    df['Amount_scaled'] = scaler.fit_transform(df[['Amount']])
    
    # We use V1-V28 + deviation + Amount_scaled (30 features total)
    features = [f'V{i}' for i in range(1, 29)] + ['deviation', 'Amount_scaled']
    X = df[features]
    y = df['Class']

    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)

    model = RandomForestClassifier(n_estimators=50, max_depth=10, n_jobs=-1)
    model.fit(X_res, y_res)

    joblib.dump(model, "models/fraud_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    print("Success: Model Trained with Behavioral Features!")

if __name__ == "__main__":
    train_model()