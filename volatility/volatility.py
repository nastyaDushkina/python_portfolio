# -*- coding: utf-8 -*-


import zipfile
import os.path

FILE_NAME = 'trades.zip'


class Ticker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.name = os.path.basename(self.file_path).split('.')[0]
        self.prices = []
        self.volatility_inf = None

    def run(self):
        with open(self.file_path, 'r') as file:
            file.readline()
            for line in file:
                ticker_inf = line.split(',')
                self.prices.append(float(ticker_inf[2]))

        min_price = min(self.prices)
        max_price = max(self.prices)
        volatility = round(((max_price - min_price) / ((max_price + min_price) / 2) * 100), 2)
        self.volatility_inf = (self.name, volatility)


class TickerStore:
    def __init__(self, file_name):
        self.file_name = file_name
        self.working_directory = self.file_name.split('.')[0]
        self.volatilities = []
        self.zero_volatilities = []

    def prepare_store(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for file in zfile.namelist():
            zfile.extract(file)

    def get_ticker(self):
        trade_files = os.listdir(self.working_directory)
        self.tickers = [Ticker(file_path=os.path.join(self.working_directory, file)) for file in trade_files]

    def get_volatility(self):
        self.volatilities = [ticker.volatility_inf for ticker in self.tickers]
        self.volatilities.sort(key=lambda x: x[1])
        # print(self.tickers_volatility)

    def get_null_volatility(self):
        self.volatilities.reverse()
        # print(len(self.tickers_volatility))

        while len(self.volatilities):
            if not self.volatilities[-1][1]:
                self.zero_volatilities.append(self.volatilities.pop())
            else:
                break
        # print(len(self.tickers_volatility))
        self.zero_volatilities.sort(key=lambda x: x[0].split('_')[1])
        # print(self.ticker_null_volatility)
        self.volatilities.reverse()
        # print(self.tickers_volatility)

    def print_result(self):
        print('Максимальная волатильность:')
        for i in range(3):
            print(f'{self.volatilities[-1 - i][0]} - {self.volatilities[-1 - i][1]} %')
        print('Минимальная волатильность:')
        for i in range(3):
            print(f'{self.volatilities[i][0]} - {self.volatilities[i][1]} %')
        print('Нулевая волатильность:')
        for ticker in self.zero_volatilities:
            print(f'{ticker[0]}', end=', ')

    def run(self):
        self.prepare_store()
        self.get_ticker()

        for ticker in self.tickers:
            ticker.run()

        self.get_volatility()
        self.get_null_volatility()
        self.print_result()


ticker_store = TickerStore(FILE_NAME)
ticker_store.run()
