# import talib
import numpy as np
import time


def getTime():
    return str(int(time.time() * 1000))


def getHumanReadTime(t=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def getMA(data, N, j=0):
    '''
    通用均线计算
    :param N: N表示想获取多长时间的均线，比如获取5日均线，N传5
    :param j: j表示往前数第几天，比如想计算三天前的MA，j传-3
    :return: [MAn]
    '''
    return sum(float(d[4]) for d in data[-1 - N + j: -1 + j]) / float(N)


def getBoll(data, j=0, P=2, N=20):
    '''
    一般情况下，设定N=20和K=2，这两个数值也是在布林带当中使用最多的。
    在日线图里，N=20其实就是“月均线”（MA20）。
    依照正态分布规则，约有95%的数值会分布在距离平均值有正负2个标准差(±2σ)的范围内。
    :param N: N代表一个时间段
    :param K: K代表几倍标准差
    :param j: j表示往前数第几天，比如想计算昨天的MA，j传-1
    :return: [中轨值, 上轨值, 下轨值, %b指标, 宽带指标]
    '''
    MB = getMA(data, N)
    delta = P * np.std([float(d[4]) for d in data[-1 - N + j: -1 + j]])
    UP = MB + delta
    LB = MB - delta
    PB = (float(data[-1 + j][4]) - LB) / (UP - LB)
    BW = (UP - LB) / MB
    return [MB, UP, LB, PB, BW]


# def macdjincha(data):
#     close = [float(x[4]) for x in data]
#     df = {}
#     # 调用talib计算指数移动平均线的值
#     # df['EMA12'] = talib.EMA(np.array(close), timeperiod=12)
#     # df['EMA26'] = talib.EMA(np.array(close), timeperiod=26)
#     # 调用talib计算MACD指标
#     df['DIF'], df['DEM'], df['D-M'] = talib.MACD(np.array(close), fastperiod=12, slowperiod=26,
#                                                  signalperiod=9)
#     # 金叉或者死叉
#     if df['DIF'][-1] - df['DEM'][-1] > 0.1 and df['DIF'][-2] - df['DEM'][-2] < -0.1:
#         return 'up'
#     elif df['DIF'][-1] - df['DEM'][-1] < -0.1 and df['DIF'][
#         -2] - df['DEM'][-2] > 0.1:
#         return 'down'


def pianli(data):
    MA30 = getMA(data, 30)
    currentPrice = float(data[-1][4])
    ratio = abs(currentPrice - MA30) / MA30
    if ratio > 0.05 and currentPrice > MA30:
        return 'down'
    elif ratio > 0.05 and currentPrice < MA30:
        return 'up'
    return ''


def isNeedle(dataItem):
    start = dataItem[1]
    highest = dataItem[2]
    lowest = dataItem[3]
    end = dataItem[4]
    max = max(start, end)
    min = min(start, end)
    if (highest - max) / max > 0.008 or (min - lowest) / min > 0.008:
        return True
    return False


def isBigNeedle(dataItem):
    start = dataItem[1]
    highest = dataItem[2]
    lowest = dataItem[3]
    end = dataItem[4]
    max = max(start, end)
    min = min(start, end)
    if (highest - max) / max > 0.012 or (min - lowest) / min > 0.012:
        return True
    return False


def updateKline(kline, message):
    newItem = [message['k']['t'], message['k']['o'], message['k']['h'], message['k']['l'],
               message['k']['c'],
               message['k']['v'], message['k']['T'], message['k']['q'], message['k']['n'],
               message['k']['V'],
               message['k']['Q'], message['k']['B']]
    if kline[-1][0] != message['k']['t']:
        kline.append(newItem)
        del kline[0]
    else:
        kline[-1] = newItem
    return kline
