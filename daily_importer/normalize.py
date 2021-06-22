import sys
from src.Candles.RawToNormalized import RawToNormalized
from src.Persistence.Database import Database
from src.Repositories.NormalizedCandlesRepository import NormalizedCandlesRepository
from src.Repositories.RawCandlesRepository import RawCandlesRepository

if len(sys.argv) < 3:
    print("Need to specify the pair you want to fetch and the timeframe")
    exit()

pair = sys.argv[1]
timeframe = sys.argv[2]

db = Database()
raw_candles_repository = RawCandlesRepository(db)
normal_candles_repository = NormalizedCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

# Convert to differentials

converter = RawToNormalized(raw_candles)
normal_candles = converter.convert()

# Store

normal_candles_repository.store(pair, timeframe, normal_candles)


