import numpy as np
import sys
from tensorflow.keras.utils import to_categorical
from src.ModelBuilder import ModelBuilder
from src.Persistence.Database import Database
from src.Preprocess.BalancedSampler import BalancedSampler
from src.Repositories.RawDataRepository import RawDataRepository

from src.Preprocess.Sampler import Sampler

if len(sys.argv) < 6:
    print("Missing arguments!")
    exit()

pair = sys.argv[1]
timeframe = sys.argv[2]
from_date = sys.argv[3]
to_date = sys.argv[4]
name = sys.argv[5]
samples_name = f"{pair}_{timeframe}.npy"

create_sequences = True

if create_sequences:

    # Load raw data
    raw_candles_repository = RawDataRepository(Database())
    df = raw_candles_repository.get(pair, timeframe, from_date, to_date)

    sampler = BalancedSampler(Sampler())
    # sampler = Sampler()
    x_train, y_train = sampler.sample(timeframe, df)

    y_train = to_categorical(y_train, 3)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    np.save(f"samples/x_{samples_name}", x_train)
    np.save(f"samples/y_{samples_name}", y_train)
else:
    x_train = np.load(f"samples/x_{samples_name}")
    y_train = np.load(f"samples/y_{samples_name}")

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

ModelBuilder.build(x_train, y_train, name)
