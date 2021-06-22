import sys
from src.Candles.RawToNormalized import RawToNormalized
from src.Persistence.Database import Database
from src.Repositories.NormalizedCandlesRepository import NormalizedCandlesRepository
from src.Repositories.RawCandlesRepository import RawCandlesRepository

pair = 'ETHUSD'
timeframe = 15

db = Database()
raw_candles_repository = RawCandlesRepository(db)
normal_candles_repository = NormalizedCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

# Convert to differentials

converter = RawToNormalized(raw_candles)
normal_candles = converter.convert()

arr_normal_candles = normal_candles.array()

batch_size = 100
delay_size = 4
price_increment = 0.06
set_size = len(arr_normal_candles)

for i in range(batch_size, set_size):
    from_index = i - batch_size
    to_index = i - 1
    target_index = to_index + delay_size
    if target_index >= set_size:
        break

    first_element = arr_normal_candles[from_index]
    last_element = arr_normal_candles[to_index]
    target_element = arr_normal_candles[target_index]

    diff = 0
    for index in range(to_index + 1, target_index + 1):
        diff = diff + arr_normal_candles[index].close()

    if diff >= price_increment or diff * -1 >= price_increment:
        variance = diff / price_increment
        if variance > 1:
            variance = 1
        if variance < -1:
            variance = -1
        print(from_index, to_index, variance)

print(set_size)
