import akshare as ak
from akshare.stock.stock_summary import stock_szse_summary

# 需要：总市值 上市股票数量
stock_sse_summary_df = ak.stock_sse_summary()
stock_szse_summary_df = ak.stock_szse_summary(date="20220610")
print(stock_sse_summary_df)
print(stock_szse_summary_df)

# 社会融资规模
macro_china_shrzgm_df = ak.macro_china_shrzgm()
print(macro_china_shrzgm_df)

# m2
macro_china_m2_yearly_df = ak.macro_china_m2_yearly()
print(macro_china_m2_yearly_df)

# 社会消费品零售总额
# macro_china_consumer_goods_retail_df = ak.acro_china_consumer_goods_retail()
# print(macro_china_consumer_goods_retail_df)

# 融券
stock_margin_sse_df = ak.stock_margin_sse(start_date="20210208", end_date="20210208")
print(stock_margin_sse_df)
stock_margin_sse_df = ak.stock_margin_szse(date="20210401")
print(stock_margin_sse_df)