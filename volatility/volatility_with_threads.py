# -*- coding: utf-8 -*-


import time
import zipfile
import os.path
from threading import Thread

FILE_NAME = 'trades.zip'


class Ticker(Thread):
    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        self.ticker_name = os.path.basename(self.file_path).split('.')[0]
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
        self.volatility_inf = (self.ticker_name, volatility)


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

    def process_ticker_inf(self):
        for ticker in self.tickers:
            ticker.run()

    def run(self):
        self.prepare_store()
        self.get_ticker()
        self.process_ticker_inf()
        self.get_volatility()
        self.get_null_volatility()
        self.print_result()


class TickerStoreMultithreaded(TickerStore):
    def process_ticker_inf(self):
        for ticker in self.tickers:
            ticker.start()

        for ticker in self.tickers:
            ticker.join()


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        print(f'\nФункция {func.__name__} работала {elapsed} секунд(ы)')
        return result

    return surrogate


@time_track
def prepare_report_volatility(data_store):
    # ticker_store = TickerStore(data_store)
    ticker_store = TickerStoreMultithreaded(data_store)
    ticker_store.run()


prepare_report_volatility(FILE_NAME)
