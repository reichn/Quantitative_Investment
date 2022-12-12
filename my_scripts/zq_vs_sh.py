import tushare as ts
import datetime as dt
import matplotlib.pyplot as plt

ts.set_token('a8e773947efb1cf732c5258f45b3de232206cd541706bce0fb447779')
pro = ts.pro_api()

today = dt.date.today().strftime("%Y%m%d")
pre_day = (dt.date.today() - dt.timedelta(days=100)).strftime("%Y%m%d")

zq = pro.ths_daily(ts_code='881157.TI', start_date=pre_day, end_date=today,
                   fields='ts_code,trade_date,open,close,high,low,pct_change')

sh = pro.index_daily(ts_code='000001.SH', start_date=pre_day, end_date=today)

dif = zq['pct_change'] - sh['pct_chg']
ax = dif.plot.bar()
plt.show()
