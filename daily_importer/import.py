import sys

from src.Candles.RawToDifferential import RawToDifferential
from src.Repositories.Finance import Finance
from src.Persistence.Database import Database
from src.Repositories.RawCandlesRepository import RawCandlesRepository

if len(sys.argv) < 3:
    print("Need to specify the pair you want to fetch and the timeframe")
    exit()

pair = sys.argv[1]
timeframe = sys.argv[2]

db = Database()
raw_candles_repository = RawCandlesRepository(db)

# Fetch new data

fetcher = Finance(pair, timeframe)
fetcher.load()
candles = fetcher.candles()

# Store

raw_candles_repository.store(pair, timeframe, candles)