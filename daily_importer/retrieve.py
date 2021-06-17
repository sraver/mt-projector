import sys
from src.Candles.SourceToNormalized import SourceToNormalized
from src.Persistence.Database import Database
from src.Repositories.NormalizedCandlesRepository import NormalizedCandlesRepository
from src.Repositories.SourceCandlesRepository import SourceCandlesRepository

if len(sys.argv) < 3:
    print("Need to specify the pair you want to fetch and the timeframe")
    exit()

pair = sys.argv[1]
timeframe = sys.argv[2]

db = Database()
source_candles_repository = SourceCandlesRepository(db)
normal_candles_repository = NormalizedCandlesRepository(db)

# Load raw data

source_candles = source_candles_repository.get(pair, timeframe)

# Convert to differentials

converter = SourceToNormalized(source_candles)
normal_candles = converter.convert()

# Store
normal_candles_repository.store(pair, timeframe, normal_candles)


