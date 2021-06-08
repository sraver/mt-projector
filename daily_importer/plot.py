import sys
import finplot as fplt
import pandas as pd
from src.Candles.RawToDifferential import RawToDifferential
from src.Persistence.Database import Database
from src.Repositories.RawCandlesRepository import RawCandlesRepository

if len(sys.argv) < 3:
    print("Need to specify the pair you want to fetch and the timeframe")
    exit()

sys.setrecursionlimit(1000000)

pair = sys.argv[1]
timeframe = sys.argv[2]

db = Database()
raw_candles_repository = RawCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

# Convert to differentials

converter = RawToDifferential(raw_candles)
diff_candles = converter.convert()

# Create data structure for plot

array_diff_candles = diff_candles.array()

arr_open = []
arr_close = []
arr_high = []
arr_low = []

for row in array_diff_candles:
    open_value = row.open()
    high_value = open_value + row.high_difference()
    low_value = open_value + row.low_difference()
    close_value = open_value + row.close_difference()
    arr_open.append(open_value)
    arr_high.append(high_value)
    arr_low.append(low_value)
    arr_close.append(close_value)

data = {
    'Open': arr_open,
    'Close': arr_close,
    'High': arr_high,
    'Low': arr_low
}

rng = pd.date_range(array_diff_candles[0].date(), periods=len(array_diff_candles), freq='15T')

df = pd.DataFrame(data, columns=['Open', 'Close', 'High', 'Low'], index=rng)

# Show plot

fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
fplt.show()
