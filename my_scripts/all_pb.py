import tushare as ts
import matplotlib.pyplot as plt
import math

ts.set_token('a8e773947efb1cf732c5258f45b3de232206cd541706bce0fb447779')
pro = ts.pro_api()

df = pro.daily_basic(ts_code='', trade_date='20221209', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
pb_list = list(df['pb'])
plt.hist(pb_list, [1, 5, 10, 15, 20, 25, 30])
plt.show()

print(df['pb'].mean())

wait = input()
