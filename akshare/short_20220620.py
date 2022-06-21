from daily_data_20220617 import short
import datetime

if __name__ == "__main__":
    t = datetime.date.today().strftime("%Y%m%d")
    d = input(f"enter the day (today: {t}): ") or t
    print(short(d))
