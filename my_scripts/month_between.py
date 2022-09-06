"""
输入 2019 1 和 2015 9
返回这两个月份之间有多少个月。
"""

from datetime import datetime, timedelta


def main():
    month1 = input("input first")  # format: 2015-09-01
    month2 = input("input second")
    d1 = datetime.fromisoformat(month1)
    d2 = datetime.fromisoformat(month2)
    t = d2 - d1
    print(t / timedelta(days=30))


if __name__ == "__main__":
    main()
    print("done.")
