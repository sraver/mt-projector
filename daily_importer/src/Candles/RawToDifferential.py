from src.Candles.Raw.RawCandles import RawCandles
from src.Candles.Differential.DifferentialCandle import DifferentialCandle
from src.Candles.Differential.DifferentialCandles import DifferentialCandles


class RawToDifferential:
    def __init__(self, candles: RawCandles):
        self.__rawCandles = candles

    def convert(self) -> DifferentialCandles:
        pair = self.__rawCandles.pair()
        array_raw_candles = self.__rawCandles.array()
        array_differential_candles = []

        for i in range(1, len(array_raw_candles)):
            previous_candle = array_raw_candles[i - 1]
            current_candle = array_raw_candles[i]
            datetime = current_candle.date()
            previous_close = previous_candle.close()

            # Differential values are computed against Open price
            diff_close = current_candle.close() - previous_close
            diff_high = current_candle.high() - previous_close
            diff_low = current_candle.low() - previous_close

            ema50 = self.__compute_ema(array_raw_candles, 50, i)
            ema200 = self.__compute_ema(array_raw_candles, 200, i)

            # Differential EMAs are computed against Close price, bc EMA is computed with the close value
            diff_ema50 = ema50 - current_candle.close()
            diff_ema200 = ema200 - current_candle.close()

            differential_candle = DifferentialCandle(
                datetime, previous_close, diff_close, diff_high, diff_low, diff_ema50, diff_ema200
            )
            array_differential_candles.append(differential_candle)

        return DifferentialCandles(pair, array_differential_candles)

    def __compute_ema(self, arr_candles, ema_period, current_index):
        if current_index == 0:
            ema = arr_candles[current_index].close()
        else:
            k = 2 / (ema_period + 1)
            item = arr_candles[current_index]
            previous_ema = self.__compute_ema(arr_candles, ema_period, current_index - 1)
            ema = (item.close() * k) + (previous_ema * (1 - k))
        return ema
