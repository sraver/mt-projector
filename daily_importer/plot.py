import sys
from src.Candles.RawToDifferential import RawToDifferential
from src.Persistence.Database import Database
from src.Repositories.Plotter import Plotter
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
Plotter.draw_chart(pair, diff_candles)
