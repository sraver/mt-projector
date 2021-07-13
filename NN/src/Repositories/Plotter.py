import finplot as fplt
import pandas as pd

from src.Candles.Differential.DifferentialCandles import DifferentialCandles


class Plotter:

    @staticmethod
    def draw_chart(pair, diff_candles: DifferentialCandles) -> None:
        array_diff_candles = diff_candles.array()
        arr_dates = []
        arr_open = []
        arr_close = []
        arr_high = []
        arr_low = []
        arr_ema50 = []
        arr_ema200 = []

        # Convert data from differential to absolute
        for row in array_diff_candles:
            open_value = row.open()
            high_value = open_value + row.high_difference()
            low_value = open_value + row.low_difference()
            close_value = open_value + row.close_difference()
            ema50 = close_value + row.ema50()
            ema200 = close_value + row.ema200()

            arr_dates.append(row.date())
            arr_open.append(open_value)
            arr_high.append(high_value)
            arr_low.append(low_value)
            arr_close.append(close_value)
            arr_ema50.append(ema50)
            arr_ema200.append(ema200)

        # Create DataFrame
        data = {
            'Time': arr_dates,
            'Open': arr_open,
            'Close': arr_close,
            'High': arr_high,
            'Low': arr_low
        }

        df = pd.DataFrame(data, columns=['Time', 'Open', 'Close', 'High', 'Low'])

        # Create plot
        ax = fplt.create_plot(pair, rows=1)

        # Feed candles data to the plot
        candles = df[['Time', 'Open', 'Close', 'High', 'Low']]
        fplt.candlestick_ochl(candles, ax=ax)

        # Create series for EMAs
        ema50_serie = pd.Series(arr_ema50, dtype='float64')
        ema200_serie = pd.Series(arr_ema200, dtype='float64')

        # Feed EMA series to the plot
        fplt.plot(df['Time'], ema50_serie, style='-', legend='EMA-50')
        fplt.plot(df['Time'], ema200_serie, style='-', legend='EMA-200')

        # Show plot
        fplt.show()
