class NormalizedCandle:
    def __init__(self, date, close, high, low, rsi, ema50, ema200, ema800):
        self.__date = date
        self.__close = close
        self.__high = high
        self.__low = low
        self.__rsi = rsi
        self.__ema50 = ema50
        self.__ema200 = ema200
        self.__ema800 = ema800

    def month_of_year(self):
        return self.__date.month

    def day_of_week(self):
        return self.__date.weekday()

    def hour(self):
        return self.__date.hour

    def date(self):
        return self.__date

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
