from math import floor

import pandas as pd

# df1 = pd.read_csv('20221017.csv')
# df2 = pd.read_csv('choice1017.csv', na_values='——')

df1 = pd.read_csv('20221018.csv')
df2 = pd.read_csv('choice1018.csv', na_values='——')

df1.reset_index()


def ratio(df_sort):
    df_sort.dropna()
    n = df_sort.shape[0]
    half = floor(n / 2)
    first_sum = df_sort["amount"].loc[:half].sum()
    second_sum = df_sort["amount"].loc[half + 1:].sum()
    out = (first_sum - second_sum) / df_sort["amount"].sum()
    return out


a = ratio(df1)
b = ratio(df2)
print("{:.2%}, {:.2%}".format(float(a), float(b)))
_ = input()
