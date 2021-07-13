import sys
import numpy as np
from src.ModelBuilder import ModelBuilder
from src.Persistence.Database import Database
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

# Load raw data
raw_candles_repository = RawDataRepository(Database())
df = raw_candles_repository.get(pair, timeframe, from_date, to_date)

# Create samples
sampler = Sampler()
x_test, y_test = sampler.sample(timeframe, df)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

print(f"x_train shape: {x_test.shape}")

# Predict
model = ModelBuilder.load(name)
y_predicted = model.predict(x_test)

model.plot_confusion_matrix(y_test, y_predicted)
