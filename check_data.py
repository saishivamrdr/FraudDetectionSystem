import pandas as pd

df = pd.read_csv("data/creditcard.csv")

print(df.head())
print()
print("Shape:", df.shape)
print()
print("Class counts:")
print(df["Class"].value_counts())