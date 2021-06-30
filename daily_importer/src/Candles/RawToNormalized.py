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

        for candle in array_raw_candles:
            close = self.percentage_difference(candle.open(), candle.close())
            high = self.percentage_difference(candle.open(), candle.high())
            low = self.percentage_difference(candle.open(), candle.low())
            ema50 = self.percentage_difference(candle.close(), candle.ema50())
            ema200 = self.percentage_difference(candle.close(), candle.ema200())
            ema800 = self.percentage_difference(candle.close(), candle.ema800())

            normalized_candle = NormalizedCandle(candle.date(), close, high, low, candle.rsi(), ema50, ema200, ema800)
            array_normalized_candles.append(normalized_candle)

        return NormalizedCandles(pair, array_normalized_candles)

    @staticmethod
    def percentage_difference(open, other):
        return (other - open) / open
