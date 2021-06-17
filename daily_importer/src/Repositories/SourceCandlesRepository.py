from src.Candles.Source.SourceCandle import SourceCandle
from src.Candles.Source.SourceCandles import SourceCandles


class SourceCandlesRepository:

    def __init__(self, db):
        self.__db = db

    def get(self, pair, timeframe) -> SourceCandles:
        rs = self.__db.execute(
            '''SELECT datetime, open, close, high, low, rsi, ema50, ema200, ema800, volume FROM test_table
                WHERE asset = %s AND period = %s''',
            (pair, timeframe)
        )
        arr = []
        for row in rs:
            datetime = row[0]
            open = row[1]
            close = row[2]
            high = row[3]
            low = row[4]
            rsi = row[5]
            ema50 = row[5]
            ema200 = row[6]
            ema800 = row[7]
            volume = row[8]
            raw_candle = SourceCandle(datetime, open, high, low, close, rsi, ema50, ema200, ema800, volume)
            arr.append(raw_candle)
        return SourceCandles(pair, arr)
