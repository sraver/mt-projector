import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.utils import shuffle


class Sampler:
    def __init__(self, period_size=60, delay_periods=4, change_threshold=0.01):
        self.__check_arguments(period_size, delay_periods, change_threshold)
        self.period_size = period_size
        self.delay_periods = delay_periods
        self.change_threshold = change_threshold

    def __check_arguments(self, period_size, delay_periods, change_threshold):
        if period_size <= 0:
            raise Exception('Period length must be greater than zero.')
        if delay_periods <= 0:
            raise Exception('Delay periods length must be greater than zero.')
        if change_threshold <= 0:
            raise Exception('Change threshold must be greater than zero.')

    def __check_data(self, df: DataFrame):
        if len(df) < self.period_size + self.delay_periods:
            raise Exception('Not enough data')

    def __default_relevant_fields(self, fields):
        if fields is None:
            return ['close', 'rsi', 'ema50', 'ema200', 'ema800']
        else:
            return fields

    def sample(self, period, df_source: DataFrame, relevant_fields=None):
        self.__check_data(df_source)
        relevant_fields = self.__default_relevant_fields(relevant_fields)

        df_percentiles = self.to_percentiles(df_source)
        df = self.normalize(df_percentiles)

        # Generate samples
        x, y = [], []
        collection_size = len(df)

        for i in range(self.period_size, collection_size):
            # Compute relevant indexes
            from_index = i - self.period_size
            to_index = i - 1
            target_index = to_index + self.delay_periods

            if target_index >= collection_size:
                break  # Out of bounds

            # Check range completeness
            current_sequence = df[from_index:target_index + 1]
            has_gaps = self.__sequence_has_gaps(current_sequence, period)

            if has_gaps:
                continue  # Current sequence invalid

            # Check sequence class-type
            direction = self.__sample_direction(df_percentiles, target_index, to_index)

            sequence = current_sequence[:-self.delay_periods][relevant_fields] \
                .to_numpy() \
                .reshape(1, -1)[0]

            x.append(sequence)
            y.append(direction)

        x = np.array(x)
        y = np.array(y)

        x, y = shuffle(x, y)

        return x, y

    def __sample_direction(self, df, target_index, to_index):
        price_change = 0
        for index in range(to_index + 1, target_index + 1):
            price_change = price_change + df.iloc[index].close

        if price_change > self.change_threshold:
            direction = 1
        elif price_change < self.change_threshold * -1:
            direction = 2
        else:
            direction = 0

        return direction

    def __sequence_has_gaps(self, current_sequence, period):
        expected_range = pd.date_range(
            current_sequence.index[0],
            periods=self.period_size + self.delay_periods,
            freq=f"{period}min"
        )
        has_gaps = expected_range[-1] != pd.to_datetime(current_sequence.index[-1])
        return has_gaps

    @staticmethod
    def to_percentiles(df: DataFrame) -> DataFrame:
        df = df.copy()

        df.ema50 = (df.ema50 - df.close) / df.close
        df.ema200 = (df.ema200 - df.close) / df.close
        df.ema800 = (df.ema800 - df.close) / df.close

        df.low = (df.low - df.open) / df.open
        df.high = (df.high - df.open) / df.open
        df.close = (df.close - df.open) / df.open

        df.rsi /= 100

        df.drop('open', axis=1, inplace=True)

        return df

    def normalize(self, df: DataFrame):
        df = df.copy()

        df['close'] = self.__scale(df['close'])
        df['ema50'] = self.__scale(df['ema50'])
        df['ema200'] = self.__scale(df['ema200'])
        df['ema800'] = self.__scale(df['ema800'])

        return df

    def __scale(self, col):
        max = 65000
        min = 3100
        return (col - min) / (max - min)
