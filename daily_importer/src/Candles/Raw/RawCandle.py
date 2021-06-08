class RawCandle:
    def __init__(self, date, open, high, low, close, volume):
        self.__date = date
        self.__open = open
        self.__high = high
        self.__low = low
        self.__close = close
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

    def volume(self):
        return self.__volume