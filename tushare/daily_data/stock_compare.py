import re

with open('1017.txt', 'r') as f1:
    first = f1.read()

with open('1017a.txt', 'r') as f2:
    second = f2.read()

pattern = r'\d{6}\.'
out_f = re.findall(pattern, first)
out_f2 = re.findall(pattern, second)
out = set(out_f) - set(out_f2)
print(out)

# tushare 自己排除了空值
# 差异是 -- 值，tushare没有，似乎是做了清理。
