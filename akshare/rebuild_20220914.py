import pathlib
from unicodedata import category


def instant_files():
    n = 0
    for file in all_file:
        if "instant" in file.name:
            n += 1
            print(n, " ", "filename:", file.name)  # 文件个数+文件名
            date = file.name[:8]
            # category = file.name[9:]
            with file.open(mode="r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                print(line)
                if "北上资金" in line:
                    with open("beixiang.txt", "a", encoding="utf-8") as fi:
                        fi.write(str(date) + " " + line + "\n")


if __name__ == "__main__":
    p = pathlib.Path("D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data")

    all_file = list(p.glob("*.txt"))
    print("------------")
    # print(all_file[0].name)

    instant_files()
