from math import floor
import datetime
import time

import akshare as ak

import warnings

warnings.filterwarnings("ignore")


def north():
    stock_hsgt_hist_em_df1 = ak.stock_hsgt_hist_em(symbol="沪股通")  # 北上
    stock_hsgt_hist_em_df2 = ak.stock_hsgt_hist_em(symbol="深股通")
    return stock_hsgt_hist_em_df1["当日成交净买额"].iloc[0] + stock_hsgt_hist_em_df2["当日成交净买额"].iloc[0]


def his_high():
    stock_rank_cxg_ths_df = ak.stock_rank_cxg_ths(symbol="历史新高")
    return stock_rank_cxg_ths_df["股票简称"]


def year_low():
    stock_rank_cxd_ths_df = ak.stock_rank_cxd_ths(symbol="一年新低")
    return stock_rank_cxd_ths_df["股票简称"]


def trade_ratio():
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    stock_zh_a_spot_em_df = stock_zh_a_spot_em_df.sort_values(by="涨跌幅", ascending=False).dropna()
    N = stock_zh_a_spot_em_df.shape[0]
    half = floor(N / 2)
    first_sum = stock_zh_a_spot_em_df["成交额"][:half].sum()
    second_sum = stock_zh_a_spot_em_df["成交额"][half + 1 :].sum()
    ratio = (first_sum - second_sum) / stock_zh_a_spot_em_df["成交额"].sum()
    return ratio


def short(day="today"):
    if day == "today":
        day = datetime.date.today().strftime("%Y%m%d")
    try:
        stock_margin_sse_df = ak.stock_margin_sse(start_date=day, end_date=day)
        margin_sse = stock_margin_sse_df["融券余量金额"].iloc[0]
        rongzi_sse = stock_margin_sse_df["融资余额"].iloc[0] / 1e8
    except ValueError:
        if day == "today":
            print("Shanghai no today's data")
        else:
            print(f"Shanghai no {day}'s data")
        return

    try:
        stock_margin_szse_df = ak.stock_margin_szse(date=day)
        margin_szse = stock_margin_szse_df["融券余额"].iloc[0]
        rongzi_szse = stock_margin_szse_df["融资余额"].iloc[0]
    except ValueError:
        if day == "today":
            print("Shenzhen no today's data")
        else:
            print(f"Shenzhen no {day}'s data")
        return

    stock_sse_summary_df = ak.stock_sse_summary()
    stock_szse_summary_df = ak.stock_szse_summary(date=day)

    num_sse = int(stock_sse_summary_df["股票"].iloc[4])
    value_sse = float(stock_sse_summary_df["股票"].iloc[1])
    num_szse = stock_szse_summary_df["数量"].iloc[0]
    value_szse = stock_szse_summary_df["总市值"].iloc[0] / 1e8

    return (margin_sse, margin_szse, value_sse, value_szse, num_sse, num_szse), (
        rongzi_sse,
        rongzi_szse,
    )


def num(m="all", day="today"):
    if day == "today":
        day = datetime.date.today().strftime("%Y%m%d")
    try:
        stock_sse_summary_df = ak.stock_sse_summary()
        stock_szse_summary_df = ak.stock_szse_summary(date=day)
        num_sse = int(stock_sse_summary_df["股票"].iloc[4])
        num_szse = stock_szse_summary_df["数量"].iloc[0]
    except (IndexError, ValueError):
        return "no " + day + "'s data"
    if m == "all":
        return (num_sse, num_szse)
    elif m == "sh":
        return num_sse
    elif m == "sz":
        return num_szse


def quick_data():
    today = datetime.date.today().strftime("%Y%m%d")
    t = time.strftime("%H:%M")
    # path = r"D:\GRC\我的坚果云\data_xlsx 数据记录\20220617 Daily data"
    path = r"D:\我的坚果云\data_xlsx 数据记录\20220617 Daily data"
    with open(path + "\\" + today + "_instant.txt", "a", encoding="utf-8") as f:
        f.write(t + "\n")
        f.write("北上资金： " + str(north()) + "\n")
        f.write("历史新高： " + str(len(list(his_high()))) + " " + " ".join(list(his_high())) + "\n")
        f.write("一年新低： " + str(len(list(year_low()))) + " " + " ".join(year_low()) + "\n")
        f.write("成交比： " + str(trade_ratio()) + "\n")
        f.write("上证股票数量： " + str(num("sh")) + "\n")
        f.write("深证股票数量： " + str(num("sz")) + "\n")
        f.write("\n")


if __name__ == "__main__":
    quick_data()
    print("done.")
    # print(short('20220617'))
