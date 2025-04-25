import pandas as pd
import os

os.makedirs("./data", exist_ok=True)
os.makedirs("./data/raw", exist_ok=True)

input_path = "../assignment-1/data/ranking.csv"
df_original = pd.read_csv(input_path)

print("Original data:")
print(df_original.head())

df_new = df_original[["Gemeinde", "final_score"]].copy()
df_new = df_new.rename(columns={"final_score": "Score"})
df_new = df_new.set_index("Gemeinde")

print("\nConverted data:")
print(df_new.head())

output_path = "./data/ranking.csv"
df_new.to_csv(output_path)

print(f"\nData successfully saved to {output_path}")
