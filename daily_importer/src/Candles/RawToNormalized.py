from src.Candles.Raw.RawCandles import RawCandles
from src.Candles.Normalized.NormalizedCandle import NormalizedCandle
from src.Candles.Normalized.NormalizedCandles import NormalizedCandles


class RawToNormalized:
    def __init__(self, candles: RawCandles):
        self.__rawCandles = candles

    def convert(self) -> NormalizedCandles:
        pair = self.__rawCandles.pair()
        array_raw_candles = self.__rawCandles.array()
        array_normalized_candles = []

        for i in range(0, len(array_raw_candles)):
            candle = array_raw_candles[i]
            close = self.get_normalized_difference(candle.open(), candle.close())
            high = self.get_normalized_difference(candle.open(), candle.high())
            low = self.get_normalized_difference(candle.open(), candle.low())
            rsi = candle.rsi() / 100
            ema50 = self.get_normalized_difference(candle.open(), candle.ema50())
            ema200 = self.get_normalized_difference(candle.open(), candle.ema200())
            ema800 = self.get_normalized_difference(candle.open(), candle.ema800())

            normalized_candle = NormalizedCandle(candle.date(), close, high, low, rsi, ema50, ema200, ema800)
            array_normalized_candles.append(normalized_candle)

        return NormalizedCandles(pair, array_normalized_candles)

    def get_normalized_difference(self, open, other):
        diff = (other - open) / open
        if diff > 1:
            diff = 1
        return diff
