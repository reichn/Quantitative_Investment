import akshare as ak
import csv
import datetime as dt
import matplotlib.pyplot as plt
from collections import Counter


def to_csv():
    zhengquan = ak.stock_board_industry_index_ths(
        symbol="证券", start_date="20200101", end_date="20220902"
    )
    a = zhengquan.sort_values(by=["成交额"]).iloc[:20, :]
    a["成交额"] = a["成交额"].div(1e8)
    b = a[["日期", "成交额"]]
    print(b)
    b.to_csv("zhengquan_volumn_2022.csv")


def years_fenbu():
    with open("zhengquan_volumn_2022.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        dates = []
        for row in reader:
            dates.append(row[1])

    dates = dates[1:]
    dates_dt = [dt.datetime.strptime(day, "%Y-%m-%d") for day in dates]
    years = [day.year for day in dates_dt]
    out = Counter(years)
    print(out)


if __name__ == "__main__":
    # to_csv()
    years_fenbu()
