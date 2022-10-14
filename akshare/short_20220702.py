# -- coding: utf-8 --

from daily_data_20220617 import short
from datetime import date, timedelta
import time


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


START = date(2014, 1, 1)
END = date(2014, 1, 10)
DIR = r"D:\我的坚果云\data_xlsx 数据记录\20220617 Daily data"

if __name__ == "__main__":
    with open(DIR + "\\" + "2014_short_debug.csv", "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M") + "\n")
        for day in date_range(START, END):
            try:
                line = short(day.strftime("%Y%m%d"))
                f.write(
                    day.strftime("%Y-%m-%d") + "," + ",".join(list(map(str, line[0][:4]))) + "\n"
                )
            except TypeError:
                continue
        f.write("\n")
