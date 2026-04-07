import pandas as pd
import os

# Ensure the data folder exists
if not os.path.exists('data'):
    os.makedirs('data')

print("⏳ Loading original dataset...")
df = pd.read_csv("data/creditcard.csv")

# 1. Create a Normal Day Audit (Low Risk)
print("Creating daily_audit_low_risk.csv...")
low_risk = df.sample(2000)
low_risk.to_csv("data/daily_audit_low_risk.csv", index=False)

# 2. Create a Breach Simulation (High Risk)
print("Creating breach_simulation_high_risk.csv...")
fraud = df[df['Class'] == 1]
normal = df[df['Class'] == 0].sample(len(fraud))
high_risk = pd.concat([fraud, normal]).sample(frac=1)
high_risk.to_csv("data/breach_simulation_high_risk.csv", index=False)

print("✅ Success! Two files created in the /data folder.")