import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/creditcard.csv")

print("First 5 rows of the dataset:")
print(df.head())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nFraud vs Normal transactions:")
print(df["Class"].value_counts())

# Plot class distribution
sns.countplot(x="Class", data=df)
plt.title("Fraud vs Normal Transactions")
plt.xticks([0, 1], ["Normal", "Fraud"])
plt.show()

# Plot transaction amount distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["Amount"], bins=50, kde=True)
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.show()