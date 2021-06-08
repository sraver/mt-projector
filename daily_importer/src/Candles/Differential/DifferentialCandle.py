class DifferentialCandle:
    def __init__(self, date, close, high, low, ema50, ema200):
        self.__date = date
        self.__close = close
        self.__high = high
        self.__low = low
        self.__ema50 = ema50
        self.__ema200 = ema200

    def date(self):
        return self.__date

    def high(self):
        return self.__high

    def low(self):
        return self.__low

    def close(self):
        return self.__close

    def ema50(self):
        return self.__ema50

    def ema200(self):
        return self.__ema200
