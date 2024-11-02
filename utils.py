import os
import pickle
import yfinance as yf


# 获取数据
def get_data(stock):
    file_path = 'data/QQQ_data.pkl'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
    else:
        data = yf.download(stock, start='2000-10-30', end='2024-10-30')
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    return data
