import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Since dataset doesn't have user ID, simulate one
df['UserID'] = df.index % 1000  # 1000 fake users

# Calculate average transaction per user
df['avg_amount_per_user'] = df.groupby('UserID')['Amount'].transform('mean')

# Calculate deviation from user average
df['amount_deviation'] = df['Amount'] / df['avg_amount_per_user']

# Flag high deviation
df['high_deviation_flag'] = df['amount_deviation'] > 2

print(df[['Amount', 'avg_amount_per_user', 'amount_deviation', 'high_deviation_flag']].head(10))