from unittest import TestCase
import pandas as pd

from src.Preprocess.BalancedSampler import BalancedSampler
from src.Preprocess.Sampler import Sampler


def get_df():
    return pd.DataFrame({
        'datetime': ['2020-01-01 00:15:00', '2020-01-01 00:30:00', '2020-01-01 00:45:00', '2020-01-01 01:00:00',
                     '2020-01-01 01:15:00', '2020-01-01 01:30:00', '2020-01-01 01:45:00', '2020-01-01 02:00:00',
                     '2020-01-01 02:15:00', '2020-01-01 02:30:00', '2020-01-01 02:45:00', '2020-01-01 03:00:00'],
        'open': [100, 200, 400, 800, 1000, 1200, 1050, 1500, 1100, 1101, 1200, 1202],
        'close': [200, 400, 800, 1000, 1200, 1050, 1500, 1100, 1101, 1200, 1202, 1000],
        'low': [100, 200, 400, 800, 1000, 1050, 1050, 1100, 1100, 1101, 1200, 1000],
        'high': [200, 400, 800, 100, 1200, 1200, 1500, 1500, 1101, 1200, 1202, 1202],
        'rsi': [50, 60, 70, 80, 50, 60, 70, 80, 50, 60, 70, 50],
        'ema50': [50, 60, 70, 80, 50, 60, 70, 80, 50, 60, 70, 50],
        'ema200': [50, 60, 70, 80, 50, 60, 70, 80, 50, 60, 70, 50],
        'ema800': [50, 60, 70, 80, 50, 60, 70, 80, 50, 60, 70, 50],
    }) \
        .set_index('datetime')


class TestBalancedSampler(TestCase):

    def test_df_with_unbalanced_samples(self):
        df = get_df()
        sampler = Sampler(period_size=3, delay_periods=1)
        x, y = sampler.sample(15, df)
        self.assertEqual(9, len(x))
        self.assertEqual(9, y.size)
        distribution = pd.DataFrame(y).value_counts().sort_index()
        self.assertNotEqual(
            distribution[0].values[0],
            distribution[1].values[0],
            distribution[2].values[0]
        )

    def test_df_with_balanced_samples(self):
        df = get_df()
        sampler = Sampler(period_size=3, delay_periods=1)
        balanced_sampler = BalancedSampler(sampler)
        x, y = balanced_sampler.sample(15, df)
        self.assertEqual(6, len(x))
        self.assertEqual(6, y.size)
        distribution = pd.DataFrame(y).value_counts().sort_index()
        self.assertEqual(
            distribution[0].values[0],
            distribution[1].values[0],
            distribution[2].values[0]
        )
