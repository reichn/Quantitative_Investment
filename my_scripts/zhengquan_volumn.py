import akshare as ak

hangye = ak.stock_board_industry_name_ths()
zhengquan = ak.stock_board_industry_index_ths(
    symbol="证券", start_date="20200101", end_date="20220902"
)
a = zhengquan.sort_values(by=["成交额"]).iloc[:20, :]
a["成交额"] = a["成交额"].div(1e8)
b = a[["日期", "成交额"]]
print(b)
