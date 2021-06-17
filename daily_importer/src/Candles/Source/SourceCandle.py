class SourceCandle:
    def __init__(self, date, open, high, low, close, rsi, ema50, ema200, ema800, volume):
        self.__date = date
        self.__open = open
        self.__high = high
        self.__low = low
        self.__close = close
        self.__rsi = rsi
        self.__ema50 = ema50
        self.__ema200 = ema200
        self.__ema800 = ema800
        self.__volume = volume

    def date(self):
        return self.__date

    def open(self):
        return self.__open

    def high(self):
        return self.__high

    def low(self):
        return self.__low

    def close(self):
        return self.__close

    def rsi(self):
        return self.__rsi

    def ema50(self):
        return self.__ema50

    def ema200(self):
        return self.__ema200

    def ema800(self):
        return self.__ema800

    def volume(self):
        return self.__volume
