from unittest import TestCase
import pandas as pd

from src.Preprocess.Sampler import Sampler


def get_df():
    return pd.DataFrame({
        'datetime': ['2020-01-01 00:15:00', '2020-01-01 00:30:00', '2020-01-01 00:45:00', '2020-01-01 01:00:00'],
        'open': [100, 200, 400, 800],
        'close': [200, 400, 800, 1000],
        'low': [100, 200, 400, 800],
        'high': [200, 400, 800, 100],
        'rsi': [50, 60, 70, 80],
        'ema50': [50, 60, 70, 80],
        'ema200': [50, 60, 70, 80],
        'ema800': [50, 60, 70, 80],
    }) \
        .set_index('datetime')


relevant_fields = ['close', 'rsi', 'ema50']


class TestSampler(TestCase):

    def test_instantiation_with_wrong_arguments(self):
        self.assertRaises(Exception, Sampler, 0, 0, 0)
        self.assertRaises(Exception, Sampler, -1, 2, 2)
        self.assertRaises(Exception, Sampler, 2, -1, 2)
        self.assertRaises(Exception, Sampler, 2, 2, -1)
        Sampler()

    def test_sampler_without_enough_data(self):
        df = get_df()
        sampler = Sampler()
        self.assertRaises(Exception, sampler.sample, 15, df)

    def test_samples_computed_with_period_3(self):
        df = get_df()
        sampler = Sampler(period_size=3, delay_periods=1)
        x, y = sampler.sample(period=15, df_source=df, relevant_fields=relevant_fields)
        self.assertEqual(1, len(x))
        self.assertEqual(9, len(x[0]))

    def test_samples_computed_with_period_2(self):
        df = get_df()
        sampler = Sampler(period_size=2, delay_periods=1)
        x, y = sampler.sample(period=15, df_source=df, relevant_fields=relevant_fields)
        self.assertEqual(2, len(x))
        self.assertEqual(6, len(x[0]))

    def test_samples_using_wrong_period(self):
        df = get_df()
        sampler = Sampler(period_size=2, delay_periods=1)
        x, y = sampler.sample(period=30, df_source=df, relevant_fields=relevant_fields)
        self.assertEqual(0, len(x))

    def test_samples_values(self):
        df = get_df()
        sampler = Sampler(period_size=3, delay_periods=1)
        x, y = sampler.sample(period=15, df_source=df, relevant_fields=relevant_fields)
        self.assertEqual(1, len(x))
        seq = x[0]
        self.assertEqual(
            [1, 0.5, 1, 1, 0.6, 1, 0.7],
            [seq[0], seq[1], round(seq[2]), seq[3], seq[4], seq[6], seq[7]]
        )
        self.assertEqual([1], [y[0]])
