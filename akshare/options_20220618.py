import requests
import datetime

url = "http://www.sse.com.cn/assortment/options/date/"
url2 = 'https://www.szse.cn/option/quotation/statistical/tabulate/'

req = requests.get(url)
req.encoding = "utf-8"
req2 = requests.get(url2)
req2.encoding = "utf-8"

day = datetime.date.today()
filename = day.strftime("%Y%m%d")

with open("option1_" + filename + ".html", 'wb') as f:
    f.write(req.content)
with open("option2_" + filename + ".html", 'wb') as f:
    f.write(req2.content)

