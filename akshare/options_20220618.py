import requests
import datetime

url = "http://www.sse.com.cn/assortment/options/date/"

req = requests.get(url)
req.encoding = "utf-8"

day = datetime.date.today()
filename = day.strftime("%Y%m%d")

with open("option" + filename + ".html", 'wb') as f:
    f.write(req.content)
