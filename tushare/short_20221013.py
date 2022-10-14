from math import floor

import tushare as ts
import datetime as dt

ts.set_token('a8e773947efb1cf732c5258f45b3de232206cd541706bce0fb447779')
pro = ts.pro_api()


def stocks_num():
    # 舍弃 deprecated 上市股票数量
    sse = pro.query('stock_basic', exchange='sse', list_status='L',
                    fields='ts_code,symbol,name,area,industry,list_date')
    szse = pro.query('stock_basic', exchange='szse', list_status='L',
                     fields='ts_code,symbol,name,area,industry,list_date')
    print(sse.shape[0], szse.shape[0], sse.shape[0] + szse.shape[0])


def margin(day=''):
    # 融券余额
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    margin_ = pro.query('margin', trade_date=day, exchange_id='')
    result = margin_[['trade_date', 'exchange_id', 'rqye']]
    return int(result.iloc[0][0]), result.iloc[0][2], result.iloc[1][2] / 1e8


def market_value(day=''):
    # 股票数量, 总市值 （深圳股票数量不准）
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    # df = pro.daily_info(trade_date=day, exchange="SH", fields="trade_date,ts_name,com_count,total_mv")
    df1 = pro.daily_info(trade_date=day, fields="trade_date,ts_name,ts_code, com_count,total_mv")
    # print(df1)
    sh_a = df1.loc[df1['ts_name'] == '上海A股']
    sh_b = df1.loc[df1['ts_name'] == '上海B股']
    sh_kc = df1.loc[df1['ts_name'] == '科创板']
    sh_num = int(sh_a['com_count']) + int(sh_b['com_count']) + int(sh_kc['com_count'])
    sh_value = float(sh_a['total_mv']) + float(sh_b['total_mv']) + float(sh_kc['total_mv'])

    sz = df1.loc[df1['ts_name'] == '深圳市场']
    sz_num = int(sz['com_count'])
    sz_value = float(sz['total_mv'])

    return int(day), sh_num, sz_num, sh_value, sz_value


def rong_zi(day=''):
    # 融资余额
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today

    margin_ = pro.query('margin', trade_date=day, exchange_id='')
    result = margin_[['trade_date', 'exchange_id', 'rzye']]
    return int(result.iloc[0][0]), result.iloc[0][2] / 1e8, result.iloc[1][2] / 1e8


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
    return str(ratio * 100)[:6] + '%'


def north(day=''):
    # 北向资金
    today = dt.date.today().strftime("%Y%m%d")
    if not day:
        day = today
    df = pro.query('moneyflow_hsgt', trade_date=day)
    return int(df['trade_date']), float(df['north_money']) / 100


if __name__ == "__main__":
    # print(stocks_num())
    # print(margin('20221013'))
    # print(market_value('20221013'))
    # print(rong_zi('20221013'))
    # print(north('20221013'))
    print(trade_ratio('20221013'))
