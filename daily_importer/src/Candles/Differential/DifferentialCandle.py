class DifferentialCandle:
    def __init__(self, date, open, close_dif, high_dif, low_dif, ema50, ema200):
        self.__date = date
        self.__open = open
        self.__close_difference = close_dif
        self.__high_difference = high_dif
        self.__low_difference = low_dif
        self.__ema50 = ema50
        self.__ema200 = ema200

    def date(self):
        return self.__date

    def open(self):
        return self.__open

    def high_difference(self):
        return self.__high_difference

    def low_difference(self):
        return self.__low_difference

    def close_difference(self):
        return self.__close_difference

    def ema50(self):
        return self.__ema50

    def ema200(self):
        return self.__ema200
