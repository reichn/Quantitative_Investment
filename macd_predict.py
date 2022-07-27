from decimal import Decimal


def ema12(ema12_pre, close):
    return (11 * ema12_pre + 2 * close) / 13


def ema26(ema26_pre, close):
    return (25 * ema26_pre + 2 * close) / 27


def dea9(dea9_pre, dif):
    return (8 * dea9_pre + 2 * dif) / 10


def dif(ema12, ema26):
    return ema12 - ema26


def macd(dif, dea):
    return 2 * (dif - dea)


def now(ema12_0, ema26_0, dea_0, close):
    ema12_1 = ema12(ema12_0, close)
    ema26_1 = ema26(ema26_0, close)
    dif_1 = dif(ema12_1, ema26_1)
    dea_1 = dea9(dea_0, dif_1)
    return ema12_1, ema26_1, dif_1, dea_1


def fn(ema12_0, ema26_0, dea_0, close):
    _, _, dif_1, dea_1 = now(ema12_0, ema26_0, dea_0, close)
    macd_ = str(macd(dif_1, dea_1))
    return Decimal(macd_).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")  # 四舍五入


def find_zero(ema12_0, ema26_0, dea_0, close_range):
    mem = -1
    for _ in close_range:
        if mem < 0 and fn(ema12_0, ema26_0, dea_0, _) > 0:
            return _
        else:
            mem = fn(ema12_0, ema26_0, dea_0, _)


def tests():
    close7 = 26.2
    assert fn(ema12_6, ema26_6, dea_6, close7) == Decimal("-1.65"), "未通过测试"
    close_ = range(35, 45)
    assert find_zero(ema12_6, ema26_6, dea_6, close_) == 40, "未通过"


# 中信建投
ema12_6 = 27.06
ema26_6 = 28.47
dea_6 = -0.34

if __name__ == "__main__":
    "待定 中信建投 7月收盘价和8月收盘价"
    tests()
    print("passed tests")

    close7 = [26, 26.5, 27]
    ema12_7 = []
    ema26_7 = []
    dea_7 = []

    for i in range(len(close7)):
        out_7 = now(ema12_6, ema26_6, dea_6, close7[i])
        ema12_7.append(out_7[0])
        ema26_7.append(out_7[1])
        dea_7.append(out_7[3])

    close8 = [30, 35, 40]
    macd_8 = []
    for i in range(len(close8)):
        for j in range(len(close7)):
            macd_8.append(fn(ema12_7[j], ema26_7[j], dea_7[j], close8[i]))

    print(macd_8)
