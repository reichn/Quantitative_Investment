from math import floor
import datetime

from black import main
import akshare as ak


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


def short():
    today = datetime.date.today().strftime("%Y%m%d")
    try:
        stock_margin_sse_df = ak.stock_margin_sse(start_date=today, end_date=today)
        margin_sse = stock_margin_sse_df["融券余量金额"]
    except ValueError:
        print("no today's data")

    try:
        stock_margin_szse_df = ak.stock_margin_szse(date=today)
        margin_szse = stock_margin_szse_df["融券余额"]
    except ValueError:
        print("no today's data")

    stock_sse_summary_df = ak.stock_sse_summary()
    stock_szse_summary_df = ak.stock_szse_summary(date=today)

    num_sse = stock_sse_summary_df["股票"].iloc[4]
    value_sse = stock_sse_summary_df["股票"].iloc[1]
    num_szse = stock_szse_summary_df["数量"].iloc[0]
    value_szse = stock_szse_summary_df["总市值"].iloc[0]

    return (margin_sse, margin_szse, value_sse, value_szse, num_sse, num_szse)


if __name__ == "__main__":
    print("北上", north())
    print("历史新高", his_high())
    print("一年新低", year_low())
    print("成交比", trade_ratio())
    print("上证融券余额", "深证融券余额", "上证总市值", "深证总市值", "上证股票数量", "深证股票数量", short())
