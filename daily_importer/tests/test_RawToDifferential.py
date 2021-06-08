from unittest import TestCase

from src.Candles.Raw.RawCandle import RawCandle
from src.Candles.Raw.RawCandles import RawCandles
from src.Candles.RawToDifferential import RawToDifferential


def many_candles(n):
    array = []
    for i in range(0, n):
        c = RawCandle('2020-10-10', 1, 2, 3, 4, 5)
        array.append(c)
    return array


def custom_candles():
    array = []
    c = RawCandle('2020-10-10', 1, 550, 1, 500, 5)
    array.append(c)
    c = RawCandle('2020-10-10', 500, 1250, 450, 1000, 5)
    array.append(c)
    c = RawCandle('2020-10-10', 1000, 2200, 900, 2000, 5)
    array.append(c)
    c = RawCandle('2020-10-10', 2000, 4300, 1500, 4000, 5)
    array.append(c)
    return array


class TestRawToDifferential(TestCase):

    def test_convert_1_candle_returns_none(self):
        raw_candles = RawCandles('ETH-USD', many_candles(1))
        converter = RawToDifferential(raw_candles)
        diff_candles = converter.convert()
        self.assertEqual(0, len(diff_candles.array()))

    def test_convert_300_candles_returns_299(self):
        raw_candles = RawCandles('ETH-USD', many_candles(300))
        converter = RawToDifferential(raw_candles)
        diff_candles = converter.convert()
        self.assertEqual(299, len(diff_candles.array()))

    def test_emas_compute(self):
        raw_candles = RawCandles('ETH-USD', custom_candles())
        converter = RawToDifferential(raw_candles)
        diff_candles = converter.convert()
        array = diff_candles.array()

        first_candle = array[0]
        self.assertEqual(-480.3921568627451, first_candle.ema50())
        # self.assertEqual(519.6078431372549, ema50)

        second_candle = array[1]
        self.assertEqual(-1422.3375624759708, second_candle.ema50())
        # self.assertEqual(577.6624375240292, ema50)

        third_candle = array[2]
        self.assertEqual(-3288.1282463004427, third_candle.ema50())
        # self.assertEqual(711.8717536995575, ema50)

    def test_differentials_compute(self):
        raw_candles = RawCandles('ETH-USD', custom_candles())
        converter = RawToDifferential(raw_candles)
        diff_candles = converter.convert()
        array = diff_candles.array()

        first_candle = array[0]
        self.assertEqual(500, first_candle.close())
        self.assertEqual(750, first_candle.high())
        self.assertEqual(-50, first_candle.low())

        second_candle = array[1]
        self.assertEqual(1000, second_candle.close())
        self.assertEqual(1200, second_candle.high())
        self.assertEqual(-100, second_candle.low())

        third_candle = array[2]
        self.assertEqual(2000, third_candle.close())
        self.assertEqual(2300, third_candle.high())
        self.assertEqual(-500, third_candle.low())
