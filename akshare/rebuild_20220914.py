import pathlib


def init():
    p = pathlib.Path("D:\\我的坚果云\\data_xlsx 数据记录\\20220617 Daily data")
    all_files = list(p.glob("*.txt"))
    print("------------")
    return all_files


def instant_files():
    n = 0
    all_files = init()
    for file in all_files:
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


def short_files():
    n = 0
    all_files = init()
    for file in all_files:
        if "short" in file.name:
            n += 1
            if n < 18:  # 从7-11开始
                continue
            print(n - 17, " ", "filename:", file.name)  # 文件个数+文件名
            date = file.name[:8]

            with file.open(mode="r", encoding="utf-8") as f:
                lines = f.readlines()

            result = []
            for line in lines:
                print(line)
                if "融券" in line:
                    if "no data" not in line:
                        result.append(line)
                        with open("short_recover_20220915.txt", "a", encoding="utf-8") as fi:
                            if result:
                                fi.write(str(date) + " " + result[-1] + "\n")
                                continue
                            else:
                                fi.write(str(date) + " " + "\n")


def del_blank_line():
    with open("short_recover_20220915.txt", "r", encoding="utf-8") as fi:
        lines = fi.readlines()

    with open("short_recover_20220915.txt", "w", encoding="utf-8") as fi:
        for line in lines:
            if len(line) != 1:
                fi.write(line)


if __name__ == "__main__":
    # instant_files()
    # short_files()
    # del_blank_line()
