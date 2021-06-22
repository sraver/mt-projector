from unittest import TestCase
from src.Candles.Raw.RawCandle import RawCandle
from src.Candles.Raw.RawCandles import RawCandles


class TestRawCandles(TestCase):

    def test_candle_values_construction(self):
        candle = RawCandle('2020-01-01', 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.assertEqual(candle.date(), '2020-01-01')
        self.assertEqual(candle.open(), 1)
        self.assertEqual(candle.high(), 2)
        self.assertEqual(candle.low(), 3)
        self.assertEqual(candle.close(), 4)
        self.assertEqual(candle.volume(), 9)

    def test_candles_construction(self):
        array = []
        c1 = RawCandle('2020-01-01', 1, 2, 3, 4, 5, 6, 7, 8, 9)
        c2 = RawCandle('2020-01-01', 1, 2, 3, 4, 5, 6, 7, 8, 9)
        array.append(c1)
        array.append(c2)
        candles = RawCandles('eth', array)
        self.assertEqual(candles.pair(), 'eth')
        self.assertEqual(len(candles.array()), 2)


