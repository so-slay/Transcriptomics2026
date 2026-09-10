import pandas as pd 

df1 = pd.read_csv("microarrays_hypoxia.csv", sep=";")
print(df1.head())
df2 = pd.read_csv("rnaseq_hypoxia.csv", sep=";")
print(df2.head())
common = df1.index.intersection(df2.index)

df1_common = df1.loc[common]
print(df1_common)

df1_common.to_csv("intersectionHypoxia.csv", sep=";", index=True)