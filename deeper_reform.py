from ast import parse
import requests
import re
import datetime as dt


def get_dates():
    url = "https://zh.m.wikipedia.org/wiki/%E4%B8%AD%E5%A4%AE%E5%85%A8%E9%9D%A2%E6%B7%B1%E5%8C%96%E6%94%B9%E9%9D%A9%E5%A7%94%E5%91%98%E4%BC%9A"

    proxy = {"https": "127.0.0.1:7890"}
    r = requests.get(url, proxies=proxy)
    p = re.compile("\d{4}年\d{1,2}月\d{1,2}日")

    a = p.findall(r.text)
    print(a)
    with open("deeper_reform.txt", "a") as f:
        for date in set(a):
            f.write(date + "\n")


def parse_dates():
    with open("deeper_reform.txt", "r") as f:
        all = f.read()
    all_dt = []
    for date in all.split():
        all_dt.append(dt.datetime.strptime(date, "%Y年%m月%d日"))
    return sorted(all_dt)


def month_each():
    all_dt = parse_dates()

    month = [0] * 12
    for date in all_dt:
        month[date.month - 1] += 1

    print("各月份开会次数：", month)


if __name__ == "__main__":
    # get_dates()
    # month_each()
    all_dt = parse_dates()
    gap_between = []
    for i in range(len(all_dt) - 1):
        t = all_dt[i + 1] - all_dt[i]
        gap_between.append(t.days)
    print(sorted(gap_between))
