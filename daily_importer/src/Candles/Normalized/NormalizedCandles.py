class NormalizedCandles:

    def __init__(self, pair, array: []):
        self.__pair = pair
        self.__candles = array

    def pair(self):
        return self.__pair

    def array(self):
        return self.__candles
