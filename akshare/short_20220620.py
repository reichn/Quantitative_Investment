from typing import Type
from daily_data_20220617 import short
import datetime
import time

""" 默认值是 昨天 """

if __name__ == "__main__":
    t = datetime.date.today().strftime("%Y%m%d")
    y = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    ti = time.strftime("%H:%M")

    d = input(f"enter the day (today: {t}=1, yestoday: {y}=2): ")
    if d == "1":
        d = t
    elif d == "2":
        d = y
    # else:
    # d = t  # 默认值

    path = r"D:\GRC\我的坚果云\data_xlsx 数据记录\20220617 Daily data"
    with open(path + "\\" + d + "_short.txt", "a", encoding="utf-8") as f:
        f.write(ti + "\n")

        try:
            f.write("融券、总市值、上市股票数量: " + str(short(d)[0]) + "\n")
        except TypeError:
            f.write("融券、总市值、上市股票数量: " + "no data" + "\n")
        try:
            f.write("融资余额: " + str(short(d)[1]) + "\n")
        except TypeError:
            f.write("融资余额: " + "no data" + "\n")

        f.write("\n")
