import sys
import numpy as np
import pandas as pd


ALPHA = 0.05

df = pd.read_csv('result.csv')

df_cleaned = df.loc[df.ir_bo!=0]

df_sorted = df_cleaned.sort_values('p_value')

np_df = df_sorted.values
nums = len(np_df)

nums_positive = 0
for i, row in enumerate(df_sorted.values):
    if nums/(i+1)*row[3] < ALPHA:
        nums_positive += 1
        print(row)
        print(nums/(i+1)*row[3])
        print('')

print(nums_positive)




