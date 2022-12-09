from ast import parse
import requests
import re
import datetime as dt
import matplotlib.pyplot as plt
import locale
from collections import Counter


def get_dates(method="local"):
    if method != "local":
        url = "https://zh.m.wikipedia.org/wiki/%E4%B8%AD%E5%A4%AE%E5%85%A8%E9%9D%A2%E6%B7%B1%E5%8C%96%E6%94%B9%E9%9D%A9%E5%A7%94%E5%91%98%E4%BC%9A"

        proxy = {"https": "127.0.0.1:7890"}
        r = requests.get(url, proxies=proxy)
        p = re.compile("\d{4}年\d{1,2}月\d{1,2}日")

        a = p.findall(r.text)
        print(a)

    else:
        with open("中央全面深化改革委员会.txt", "r", encoding="utf-8") as f:
            r = f.read()
            p = re.compile("\d{4}年\d{1,2}月\d{1,2}日")
            a = p.findall(r)

    with open("deeper_reform.txt", "w") as f:
        for date in set(a):
            f.write(date + "\n")


def parse_dates():
    with open("deeper_reform.txt", "r", encoding="gb2312") as f:
        all_ = f.read()
    all_dt = []
    for date in all_.split():
        all_dt.append(dt.datetime.strptime(date, "%Y年%m月%d日"))
    return sorted(all_dt)


def sort_datefile():
    locale.setlocale(locale.LC_ALL, "zh_CN.UTF8")
    with open("deeper_reform.txt", "r") as f:
        all_ = f.read()
    all_dt = []
    for date in all_.split():
        all_dt.append(dt.datetime.strptime(date, "%Y年%m月%d日"))

    with open("deeper_reform_sort.txt", "w") as f:
        for d in sorted(all_dt):
            t = d.strftime("%Y年%m月%d日 %a")
            f.write(t + "\n")


def month_each():
    all_dt = parse_dates()

    month = [0] * 12
    for date in all_dt:
        month[date.month - 1] += 1

    print("各月份开会次数：", month)
    return month


def gap_between():
    all_dt = parse_dates()
    gap_between = []
    for i in range(len(all_dt) - 1):
        t = all_dt[i + 1] - all_dt[i]
        gap_between.append(t.days)
    print(gap_between)
    print(sorted(gap_between))

    till_today = (dt.datetime.today() - all_dt[-1]).days
    print("gap between last and today:", till_today)
    return gap_between, till_today


def hist_plot():
    # plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"] = ["LXGW WenKai Mono"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    plt.rcParams["figure.constrained_layout.use"] = True
    fig, axs = plt.subplots(3, 1)

    m = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    c = month_each()
    ax1 = axs[0]
    ax1.bar(m, c)
    ax1.set_title("各月会议召开次数")

    g, till_today = gap_between()
    ax2 = axs[1]
    ax2.hist(g, bins=10)
    ax2.axvline(x=till_today, color="r")
    ax2.set_title("每两次会议之间间隔天数（红色线为距上次开会天数）")

    w = []
    w_ = []
    week = ["周一", "周二", "周三", "周四", "周五"]
    with open("deeper_reform_sort.txt", "r", encoding="gb2312") as f:
        lines = f.readlines()
        for line in lines:
            w.append(line.split()[1])
    for k in week:
        w_.append(dict(Counter(w))[k])
    print(w_)

    ax3 = axs[2]
    ax3.bar(week, w_)
    ax3.set_title("开会分别在周几")
    plt.show()


if __name__ == "__main__":
    # get_dates("local")
    # sort_datefile()
    hist_plot()
