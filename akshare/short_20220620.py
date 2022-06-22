from daily_data_20220617 import short
import datetime
import time

if __name__ == "__main__":
    t = datetime.date.today().strftime("%Y%m%d")
    y = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    ti = time.strftime("%H:%M")

    d = input(f"enter the day (today: {t}=1, yestoday: {y}=2): ") or y
    if d == "1":
        d = t
    elif d == "2":
        d = y

    path = r"D:\GRC\我的坚果云\data_xlsx 数据记录\20220617 Daily data"
    with open(path + "\\" + d + "_short.txt", "a", encoding="utf-8") as f:
        f.write(ti + "\n")
        f.write("融券、总市值、上市股票数量: " + str(short(d)) + "\n")
        f.write("\n")
