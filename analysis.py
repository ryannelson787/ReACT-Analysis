import pandas as pd

df = pd.read_csv("dataset.csv")
print(df.head())

numerical_cols = ['react_3', 'react_7', 'react_14', 'react_36', 'react_43', 'react_54', 'react_72', 'react_80', 'react_84']
for col in numerical_cols:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

boolean_cols = ['react_23', 'react_31', 'react_59', 'react_79', 'react_99']
df[boolean_cols] = df[boolean_cols].astype(bool)


df.to_csv("final_data.csv", index=False)

