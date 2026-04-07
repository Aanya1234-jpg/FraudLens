import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Scale Amount
scaler = StandardScaler()
df['Amount_scaled'] = scaler.fit_transform(df[['Amount']])
df = df.drop(['Amount'], axis=1)

# Features & target
X = df.drop('Class', axis=1)
y = df['Class']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Apply SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Train model
model = LogisticRegression(max_iter=3000)
model.fit(X_train_res, y_train_res)

# Get probabilities instead of 0/1
y_probs = model.predict_proba(X_test)[:, 1]

# Convert to risk score (0–100)
risk_scores = (y_probs * 100).round(2)

# Show first 10 results
results = pd.DataFrame({
    'Actual': y_test.values,
    'Risk Score': risk_scores
})

print(results.head(10))
def risk_label(score):
    if score < 30:
        return "Low"
    elif score < 70:
        return "Medium"
    else:
        return "High"

results['Risk Level'] = results['Risk Score'].apply(risk_label)

print(results.head(10))