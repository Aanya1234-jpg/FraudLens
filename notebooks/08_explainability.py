import pandas as pd
import shap
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Simulate UserID
df['UserID'] = df.index % 1000

# Behavioural Features
df['avg_amount_per_user'] = df.groupby('UserID')['Amount'].transform('mean')
df['amount_deviation'] = df['Amount'] / df['avg_amount_per_user']
df['high_deviation_flag'] = (df['amount_deviation'] > 2).astype(int)

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

# SHAP Explainer
explainer = shap.Explainer(model, X_train_res)
shap_values = explainer(X_test[:1])

# Plot explanation
shap.plots.waterfall(shap_values[0])