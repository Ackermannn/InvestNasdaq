import matplotlib.pyplot as plt
import pandas as pd
from utils import get_data

STOCK = 'QQQ'

"""
交易策略

1. 买入信号：60日均线上穿250日均线
2. 卖出信号: 60日均线下穿250日均线

"""


# 判断是否是买点信号
def is_buy_signal(data, day):
    return data['MA60'][day] > data['MA250'][day]


# 判断是否是卖点信号
def is_sell_signal(data, day):
    return data['MA60'][day] < data['MA250'][day]


def main():
    data = get_data(STOCK)
    # 加工下数据 支要 Close

    data = pd.DataFrame(index=data.index, data=data['Close', STOCK].values, columns=['Close'])

    # 计算60日和250日均线
    data['MA60'] = data['Close'].rolling(window=60).mean()
    data['MA250'] = data['Close'].rolling(window=250).mean()

    # 时间范围
    data = data['2014-10-29':'2024-10-29']

    # 模拟交易

    # 起始资金
    ini_capital = 100
    # 初始化资金
    capital = ini_capital
    # 遇到第一买入信号全仓买入，持有到有卖出信号
    position = 0

    for day in data.index:

        if is_buy_signal(data, day) and position == 0:
            position = capital / data['Close'][day]
            capital = 0
            # data['Signal'][day] = 1
            data.loc[day, 'Signal'] = 1
        elif is_sell_signal(data, day) and position != 0:
            capital = position * data['Close'][day]
            position = 0
            data.loc[day, 'Signal'] = -1
        # 如果是最后一天，强制平仓
        if day == data.index[-1] and position != 0:
            capital = position * data['Close'][day]
            position = 0
            data.loc[day, 'Signal'] = -1

    # 计算收益率
    returns = (capital - ini_capital) / ini_capital
    # 年化回报
    annualized_returns = (1 + returns) ** (252 / len(data)) - 1
    print(f"Annualized returns: {annualized_returns:.2%}")

    # 基准
    base = ini_capital / data['Close'].iloc[0] * data['Close'].iloc[-1]
    # 年化回报
    base_annualized_returns = (base / ini_capital) ** (252 / len(data)) - 1
    print(f"Base annualized returns: {base_annualized_returns:.2%}")
    #
    # # 在k线图上画出买卖信号
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close')
    plt.plot(data['MA60'], label='MA60')
    plt.plot(data['MA250'], label='MA250')
    plt.plot(data[data['Signal'] == 1].index, data['Close'][data['Signal'] == 1], '^', markersize=5, color='r', lw=0)
    plt.plot(data[data['Signal'] == -1].index, data['Close'][data['Signal'] == -1], 'v', markersize=5, color='g', lw=0)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

'''
三年 6%

五年 12.85%

十年 8%
'''
