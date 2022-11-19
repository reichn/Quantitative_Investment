import datetime as dt
import time
from math import floor
from pathlib import Path
import sys
import tushare as ts

ts.set_token('a8e773947efb1cf732c5258f45b3de232206cd541706bce0fb447779')
pro = ts.pro_api()


def earlier_data(func):
    # 装饰器
    def wrapper(day):
        flag = 10
        d = day
        one_day = dt.timedelta(days=1)

        temp = func(day)
        while flag > 0 and 'no_data' in temp:
            d = (dt.date(int(d[:4]), int(d[4:6]), int(d[6:8])) -
                 one_day).strftime("%Y%m%d")
            temp = func(d)
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
        return int(day), 'no_data', 'no_data', 'no_data', 'no_data'
    elif 'SSE' in margin_.values and 'SZSE' not in margin_.values:
        return int(day), 'has_data', 'no_data', 'has_data', 'no_data'
    elif 'SSE' not in margin_.values and 'SZSE' in margin_.values:
        return int(day), 'no_data', 'has_data', 'no_data', 'has_data'

    result = margin_[['trade_date', 'exchange_id', 'rqye', 'rzye']]
    return int(result.iloc[0][0]), result.iloc[0][2], result.iloc[1][2] / 1e8, \
           result.iloc[0][3] / 1e8, result.iloc[1][
               3] / 1e8


@earlier_data
def market_value(day=''):
    # 股票数量, 总市值 （深圳股票数量不准）
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df = pro.daily_info(trade_date=day,
                        fields="trade_date,ts_name,ts_code, com_count,total_mv")
    # print(df)
    if df.empty:
        return int(day), 'no_data', 'no_data', 'no_data', 'no_data'
    sh_a = df.loc[df['ts_name'] == '上海A股']
    sh_b = df.loc[df['ts_name'] == '上海B股']
    sh_kc = df.loc[df['ts_name'] == '科创板']
    sh_num = int(sh_a['com_count']) + int(sh_b['com_count']) + int(
        sh_kc['com_count'])
    sh_value = float(sh_a['total_mv']) + float(sh_b['total_mv']) + float(
        sh_kc['total_mv'])

    sz = df.loc[df['ts_name'] == '深圳市场']
    sz_num = int(sz['com_count'])
    sz_value = float(sz['total_mv'])

    return int(day), sh_num, sz_num, sh_value, sz_value, int(day)


@earlier_data
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
    if df.empty:
        return int(day), 'no_data'
    # df_sort = df.sort_values(by="pct_chg", ascending=False).dropna()
    df_sort = df.sort_values(by="pct_chg", ascending=False)

    # p = Path.cwd() / "daily_data"
    # if not p.joinpath(day + '.csv').exists():
    #     df_sort.to_csv(p.joinpath(day + '.csv'))

    df_sort = df_sort.reset_index()
    del df_sort['index']
    # df1 = pd.read_csv(
    #     r'D:\GRC\GitHub2\Quantitative_Investment\tushare\daily_data\20221018'
    #     r'.csv')
    # df2 = df_sort.reset_index()['amount'] - df1['amount']
    n = df_sort.shape[0]
    half = floor(n / 2)

    global median_chg, ave_chg
    median_chg = str(df_sort.iloc[half]['pct_chg'])[:4] + "%"
    ave_chg = str(df_sort['pct_chg'].mean())[:4] + "%"

    trade_date = df['trade_date'].loc[0]
    first_sum = df_sort["amount"].loc[:half].sum()
    second_sum = df_sort["amount"].loc[half + 1:].sum()
    ratio = (first_sum - second_sum) / df_sort["amount"].sum()
    return int(trade_date), "{:.2%}".format(ratio)


@earlier_data
def north(day=''):
    # 北向资金 每天18-20点更新
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df = pro.query('moneyflow_hsgt', trade_date=day)
    if df.empty:
        return int(day), 'no_data'
    return int(df['trade_date']), "{:.2f}".format(float(df['north_money'][0]) /
                                                  100)


def data():
    # today's data
    t = time.strftime("%H:%M")
    today = dt.date.today().strftime("%Y%m%d")
    today1 = dt.date.today().strftime("%Y-%m-%d %a")

    north_ = north(today)[1]
    sh_num, sz_num, sh_value, sz_value = market_value(today)[1:]
    sh_margin, sz_margin = margin(today)[1:]
    # sh_rz, sz_rz = rong_zi(today)[1:]

    try:
        sys.getwindowsversion()
        path_ = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'
    except AttributeError:
        path_ = '/Users/ruichen/Nutstore Files/我的坚果云/data_xlsx 数据记录/20220617 Daily data'

    path = Path(path_) / today / "_data.txt"
    print(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(today1 + " " + t + "\n")  # date + week + time
        f.write("北上资金： " + str(north_) + "\n")
        # f.write("历史新高： " + str(len(list(his_high()))))
        # f.write("一年新低： " + str(len(list(year_low()))))
        # f.write("成交比： " + trade_ratio() + "\n")
        f.write("股票数量： " + str(sh_num) + "" + str(sz_num) + "\n")
        f.write("融券余额、总市值：" + str(sh_margin) + " " + str(
            sz_margin) + " " + str(sh_value) + " " + str(sz_value) + "\n")
        # f.write("融资余额： " + str(sh_rz) + " " + str(sz_rz) + "\n")
        f.write("\n")


def data_2(d=''):
    t = time.strftime("%H:%M")
    # one_day = dt.timedelta(days=1)
    global today
    today = dt.date.today().strftime("%Y%m%d")
    # yesterday = (dt.date.today() - one_day).strftime("%Y%m%d")
    today1 = dt.date.today().strftime("%Y-%m-%d %a")

    if not d:
        df = pro.trade_cal(exchange='', start_date=today)
        if df.loc[df['cal_date'] == today]['is_open'][0] == 0:
            day = df.loc[df['cal_date'] == today]['pretrade_date'][0]
        elif df.loc[df['cal_date'] == today]['is_open'][0] == 1:
            day = today
    else:
        day = d

    north_ = north(day)
    tr = trade_ratio(day)
    mv = market_value(day)
    rq = margin(day)[:3]
    rz = [rq[0]] + list(margin(day)[3:])

    file_name = str(max(list(zip(north_, tr, mv, rq))[0]))  # last date
    # try:
    #     sys.getwindowsversion()
    #     path_ = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'
    # except AttributeError:
    #     path_ = '/Users/ruichen/Nutstore Files/我的坚果云/data_xlsx 数据记录/20220617 Daily data'

    if sys.platform == 'darwin':
        path_ = '/Users/ruichen/Nutstore Files/我的坚果云/data_xlsx 数据记录/20220617 Daily data'
    elif sys.platform == 'win32':
        path_ = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'

    path = Path(path_) / (file_name + "_data.txt")
    print(path)

    # path = 'D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data'
    # path = Path("/Users/ruichen/Documents/GitHub/Quantitative_Investment/tushare")
    #       / "daily_data" / (file_name + "_data.txt")

    with open(path, "a", encoding="utf-8") as f:
        f.write(today1 + " " + t + "\n")  # date + week + time
        f.write("北上资金： " + " ".join(map(str, north_)) + "\n")
        # f.write("历史新高： " + str(len(list(his_high()))))
        # f.write("一年新低： " + str(len(list(year_low()))))
        f.write("成交比： " + " ".join(map(str, tr)) + " 涨幅中位数： " + median_chg + " 平均涨幅： " + ave_chg + "\n")  # 这个不回溯
        f.write(
            "股票数量、融券、总市值： " + " ".join(
                map(str, mv[:3])) + " | " + " ".join(
                map(str, list(rq) + list(mv[3:]))) + "\n")
        f.write("融资余额： " + " ".join(map(str, rz)) + "\n")

    with open(path, "a", encoding="utf-8") as f:
        f.write("\n")
    print('done.')


if __name__ == "__main__":
    # print(stocks_num())
    # print(margin('20221013'))
    # print(market_value('20221013'))
    # print(rong_zi('20221013'))
    # print(north('20221013'))
    # print(trade_ratio('20221013'))
    
    try:
        day = sys.argv[1]  # 20221119
    except IndexError:
        day = today

    data_2(day)
