import pandas as pd

df = pd.read_csv("apple_jobs.csv")
print(df)


print(df.info)


df.isnull().sum()