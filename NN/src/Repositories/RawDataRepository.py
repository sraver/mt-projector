import pandas as pd
from pandas import DataFrame


class RawDataRepository:

    def __init__(self, db):
        self.__db = db

    def get(self, pair, timeframe, from_date, to_date) -> DataFrame:
        rs = self.__db.execute(
            '''SELECT datetime, open, close, high, low, rsi, ema50, ema200, ema800, volume FROM test_table
                WHERE asset = %s AND period = %s AND datetime BETWEEN %s AND %s''',
            (pair, timeframe, from_date, to_date)
        )

        return pd.DataFrame(
            rs,
            columns=['datetime', 'open', 'close', 'high', 'low', 'rsi', 'ema50', 'ema200', 'ema800', 'volume']
        ) \
            .set_index('datetime')
