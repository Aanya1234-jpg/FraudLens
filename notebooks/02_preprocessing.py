import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Checking missing values:")
print(df.isnull().sum())

# Scale the Amount column
scaler = StandardScaler()
df['Amount_scaled'] = scaler.fit_transform(df[['Amount']])

# Drop original Amount column
df = df.drop(['Amount'], axis=1)

# Features (X) and target (y)
X = df.drop('Class', axis=1)
y = df['Class']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nData split completed:")
print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)