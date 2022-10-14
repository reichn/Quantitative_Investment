import datetime as dt
import time
from math import floor

import tushare as ts

ts.set_token('a8e773947efb1cf732c5258f45b3de232206cd541706bce0fb447779')
pro = ts.pro_api()


def earlier_data(func):
    # 装饰器
    def wrapper(*args, **kwargs):
        flag = 10
        one_day = dt.timedelta(days=1)
        temp = func(*args, **kwargs)
        while flag > 0 and 'no data' in temp:
            temp = func((dt.date.today() - one_day).strftime('%Y%m%d'))
            flag -= 1
        return temp

    return wrapper


def stocks_num():
    # 舍弃 deprecated 上市股票数量
    sse = pro.query('stock_basic', exchange='sse', list_status='L',
                    fields='ts_code,symbol,name,area,industry,list_date')
    szse = pro.query('stock_basic', exchange='szse', list_status='L',
                     fields='ts_code,symbol,name,area,industry,list_date')
    print(sse.shape[0], szse.shape[0], sse.shape[0] + szse.shape[0])


@earlier_data
def margin(day=''):
    # 融券余额
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    margin_ = pro.query('margin', trade_date=day, exchange_id='')
    if margin_.empty:
        return int(day), 'no data', 'no data'
    result = margin_[['trade_date', 'exchange_id', 'rqye']]
    return int(result.iloc[0][0]), result.iloc[0][2], result.iloc[1][2] / 1e8


@earlier_data
def market_value(day=''):
    # 股票数量, 总市值 （深圳股票数量不准）
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df1 = pro.daily_info(trade_date=day,
                         fields="trade_date,ts_name,ts_code, com_count,total_mv")
    # print(df1)
    sh_a = df1.loc[df1['ts_name'] == '上海A股']
    sh_b = df1.loc[df1['ts_name'] == '上海B股']
    sh_kc = df1.loc[df1['ts_name'] == '科创板']
    sh_num = int(sh_a['com_count']) + int(sh_b['com_count']) + int(
        sh_kc['com_count'])
    sh_value = float(sh_a['total_mv']) + float(sh_b['total_mv']) + float(
        sh_kc['total_mv'])

    sz = df1.loc[df1['ts_name'] == '深圳市场']
    sz_num = int(sz['com_count'])
    sz_value = float(sz['total_mv'])

    return int(day), sh_num, sz_num, sh_value, sz_value


@earlier_data
def rong_zi(day=''):
    # 融资余额
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today

    margin_ = pro.query('margin', trade_date=day, exchange_id='')
    if margin_.empty:
        return int(day), 'no data', 'no data'
    result = margin_[['trade_date', 'exchange_id', 'rzye']]
    return int(result.iloc[0][0]), result.iloc[0][2] / 1e8, result.iloc[1][
        2] / 1e8


def trade_ratio(day=''):
    # 成交比
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df = pro.daily(**{
        "ts_code": "",
        "trade_date": day,
        "start_date": "",
        "end_date": "",
        "offset": "",
        "limit": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "pct_chg",
        "amount"
    ])
    df_sort = df.sort_values(by="pct_chg", ascending=False).dropna()
    N = df_sort.shape[0]
    half = floor(N / 2)
    first_sum = df_sort["amount"][:half].sum()
    second_sum = df_sort["amount"][half + 1:].sum()
    ratio = (first_sum - second_sum) / df_sort["amount"].sum()
    return "{:.2%}".format(ratio)


@earlier_data
def north(day=''):
    # 北向资金 每天18-20点更新
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df = pro.query('moneyflow_hsgt', trade_date=day)
    if df.empty:
        return int(day), 'no data'
    return int(df['trade_date']), float(df['north_money']) / 100


def data():
    # today's data
    t = time.strftime("%H:%M")
    today = dt.date.today().strftime("%Y%m%d")
    today1 = dt.date.today().strftime("%Y-%m-%d %a")

    north_ = north(today)[1]
    sh_num, sz_num, sh_value, sz_value = market_value(today)[1:]
    sh_margin, sz_margin = margin(today)[1:]
    sh_rz, sz_rz = rong_zi(today)[1:]

    path = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'
    with open(path + "\\" + today + "_data.txt", "a", encoding="utf-8") as f:
        f.write(today1 + " " + t + "\n")  # date + week + time
        f.write("北上资金： " + str(north_) + "\n")
        # f.write("历史新高： " + str(len(list(his_high()))))
        # f.write("一年新低： " + str(len(list(year_low()))))
        f.write("成交比： " + trade_ratio() + "\n")
        f.write("股票数量： " + str(sh_num) + " " + str(sz_num) + "\n")
        f.write("融券余额、总市值：" + str(sh_margin) + " " + str(
            sz_margin) + " " + str(sh_value) + " " + str(sz_value) + "\n")
        f.write("融资余额： " + str(sh_rz) + " " + str(sz_rz) + "\n")
        f.write("\n")


def data_2():
    t = time.strftime("%H:%M")
    one_day = dt.timedelta(days=1)
    today = dt.date.today().strftime("%Y%m%d")
    # yesterday = (dt.date.today() - one_day).strftime("%Y%m%d")
    today1 = dt.date.today().strftime("%Y-%m-%d %a")

    north_ = north(today)
    mv = market_value(today)
    rq = margin(today)
    rz = rong_zi(today)

    file_name = str(max(list(zip(north_, mv, rq, rz))[0]))  # last date
    path = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'
    with open(path + "\\" + file_name + "_data.txt", "a",
              encoding="utf-8") as f:
        f.write(today1 + " " + t + "\n")  # date + week + time
        f.write("北上资金： " + " ".join(map(str, north_)) + "\n")
        # f.write("历史新高： " + str(len(list(his_high()))))
        # f.write("一年新低： " + str(len(list(year_low()))))
        f.write("成交比： " + trade_ratio() + "\n")  # 这个不回溯
        f.write("股票数量、总市值： " + " ".join(map(str, mv)) + "\n")
        f.write("融券余额：" + " ".join(map(str, rq)) + "\n")
        f.write("融资余额： " + " ".join(map(str, rz)) + "\n")
        f.write("\n")


if __name__ == "__main__":
    # print(stocks_num())
    # print(margin('20221013'))
    # print(market_value('20221013'))
    # print(rong_zi('20221013'))
    # print(north('20221013'))
    # print(trade_ratio('20221013'))
    data_2()
