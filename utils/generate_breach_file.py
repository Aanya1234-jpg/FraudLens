import pandas as pd

# 1. Load your main dataset
print("⏳ Loading original data...")
df = pd.read_csv("data/creditcard.csv")

# 2. Extract ALL fraud cases (there are only 492)
fraud = df[df['Class'] == 1]

# 3. Extract an equal number of normal cases (492) to make it look like a massive attack
normal = df[df['Class'] == 0].sample(len(fraud))

# 4. Combine them and shuffle
breach_data = pd.concat([fraud, normal]).sample(frac=1).reset_index(drop=True)

# 5. Save as the special simulation file
breach_data.to_csv("data/breach_simulation_high_risk.csv", index=False)

print("✅ Success! 'data/breach_simulation_high_risk.csv' has been created.")
print("This file contains 50% Fraud, making it perfect for your Audit demo.")