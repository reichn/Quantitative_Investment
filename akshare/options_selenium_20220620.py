from selenium import webdriver
from time import sleep
import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from tornado import web

option = ChromeOptions()
option.add_argument("--headless")
browser = webdriver.Chrome(options=option)
# browser = webdriver.Chrome()

url1 = "http://www.sse.com.cn/assortment/options/date/"
url2 = "https://www.szse.cn/option/quotation/statistical/tabulate/"

browser.get(url1)
sleep(3)

ratio_50 = browser.find_element(
    by=By.XPATH, value="/html/body/div[8]/div/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[6]"
).accessible_name
# print(ratio_50.accessible_name)

sh_put_300 = browser.find_element(
    by=By.XPATH, value="/html/body/div[8]/div/div[2]/div/div[1]/div[1]/table/tbody/tr[2]/td[5]"
).accessible_name
sh_call_300 = browser.find_element(
    by=By.XPATH, value="/html/body/div[8]/div/div[2]/div/div[1]/div[1]/table/tbody/tr[2]/td[4]"
).accessible_name
# print(sh_put_300.accessible_name)
# print(sh_call_300.accessible_name)

browser.get(url2)
sleep(3)

sz_put_300 = browser.find_element(
    by=By.XPATH,
    value="/html/body/div[1]/div[5]/div/div[2]/div/div/div[4]/div/div[2]/div[1]/div/table/tbody/tr/td[4]",
).accessible_name
sz_call_300 = browser.find_element(
    by=By.XPATH,
    value="/html/body/div[1]/div[5]/div/div[2]/div/div/div[4]/div/div[2]/div[1]/div/table/tbody/tr/td[3]",
).accessible_name
# print(sz_put_300.accessible_name)
# print(sz_call_300.accessible_name)


today = datetime.date.today().strftime("%Y%m%d")
path = r"D:\GRC\我的坚果云\data_xlsx 数据记录\20220617 Daily data"
with open(path + "\\" + today + "_option.txt", "a", encoding="utf-8") as f:
    f.write("50ETF认沽认购比: " + ratio_50 + "\n")
    f.write(
        "300ETF期权: "
        + " ".join([sh_put_300[:-3], sh_call_300[:-3], sz_put_300, sz_call_300]).replace(",", "")
    )

browser.close()
