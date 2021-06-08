import yfinance as yf
from src.Candles.Raw.RawCandle import RawCandle
from src.Candles.Raw.RawCandles import RawCandles

"""
More info about the dependency: https://pypi.org/project/yfinance/
"""


class Finance:
    def __init__(self, pair, interval):
        self.__pair = pair
        self.__period = '60d'
        self.__interval = interval
        self.__data = None

    def load(self):
        self.__data = yf.download(
            self.__pair,
            period=self.__period,
            interval=self.__interval,
            progress=False
        )

    def candles(self) -> RawCandles:
        candles = []
        for datetime, item in self.__data.iterrows():
            open_value = item[0]
            high_value = item[1]
            low_value = item[2]
            close_value = item[3]
            volume_value = item[5]
            candle = RawCandle(datetime, open_value, high_value, low_value, close_value, volume_value)
            candles.append(candle)
        return RawCandles(self.__pair, candles)
