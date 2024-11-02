import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
import pickle

STOCK = 'QQQ'

def main():
    file_path = '../data/QQQ_data.pkl'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
    else:
        data = yf.download(STOCK, start='2000-10-30', end='2024-10-30')
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)

    # 只保留需要的列 ， 只要 2021年后的数据
    data = pd.DataFrame(index=data.index, data={
        'Open': data['Open', STOCK].values,
        'High': data['High', STOCK].values,
        'Low': data['Low', STOCK].values,
        'Close': data['Close', STOCK].values,
        'Volume': data['Volume', STOCK].values
    })
    data = data['2021-1-1':'2024-10-30']
    # 绘制蜡烛图
    mpf.plot(data, type='candle', volume=True, style='charles', title=f'{STOCK} Candlestick Chart', ylabel='Price', ylabel_lower='Volume')

if __name__ == '__main__':
    main()