from src.Candles.Normalized.NormalizedCandles import NormalizedCandles


class NormalizedCandlesRepository:

    def __init__(self, db):
        self.__db = db

    def store(self, pair, period, candles: NormalizedCandles) -> None:
        for candle in candles.array():
            datetime = candle.date()
            moy = candle.month_of_year()
            dow = candle.day_of_week()
            hour = candle.hour()
            high = candle.high()
            low = candle.low()
            close = candle.close()
            rsi = candle.rsi()
            ema50 = candle.ema50()
            ema200 = candle.ema200()
            ema800 = candle.ema800()

            self.__db.execute(
                '''INSERT INTO normal_data(
                    asset, period, datetime, moy, dow, hour, close, high, low, rsi, ema50, ema200, ema800)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (pair, period, datetime, moy, dow, hour, close, high, low, rsi, ema50, ema200, ema800)
            )
