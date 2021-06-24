from src.Candles.Raw.RawCandle import RawCandle
from src.Candles.Raw.RawCandles import RawCandles


class RawCandlesRepository:

    def __init__(self, db):
        self.__db = db

    def store(self, pair, timeframe, candles: RawCandles) -> None:
        for candle in candles.array():
            datetime = candle.date()
            open = candle.open()
            high = candle.high()
            low = candle.low()
            close = candle.close()
            volume = candle.volume()

            self.__db.execute(
                '''INSERT INTO raw_data(
                    asset, timeframe, date, open, close, high, low, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (pair, timeframe, datetime, open, close, high, low, volume)
            )

    def get(self, pair, timeframe) -> RawCandles:
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
            ema50 = row[6]
            ema200 = row[7]
            ema800 = row[8]
            volume = row[9]
            raw_candle = RawCandle(datetime, open, high, low, close, rsi, ema50, ema200, ema800, volume)
            arr.append(raw_candle)
        return RawCandles(pair, arr)
