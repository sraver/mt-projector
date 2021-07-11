import numpy as np
import time
import sys
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

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

create_sequences = True

samples_name = f"{pair}_{timeframe}.npy"

if create_sequences:
    raw_candles_repository = RawDataRepository(Database())

    # Load raw data

    df = raw_candles_repository.get(pair, timeframe, from_date, to_date)

    sampler = BalancedSampler(Sampler())
    # sampler = Sampler()

    x_train, y_train = sampler.sample(timeframe, df)

    np.save(f"samples/x_{samples_name}", x_train)
    np.save(f"samples/y_{samples_name}", y_train)

else:
    x_train = np.load(f"samples/x_{samples_name}")
    y_train = np.load(f"samples/y_{samples_name}")

y_train = to_categorical(y_train, 3)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Create the model

model = Sequential()

model.add(LSTM(units=64, return_sequences=True, input_shape=x_train.shape[1:]))
model.add(Dropout(0.2))

model.add(LSTM(units=64, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=32))
model.add(Dropout(0.2))

model.add(Dense(3, activation='softmax'))

model.compile(
    optimizer=Adam(learning_rate=1e-06),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

tensorboard = TensorBoard(log_dir=f"logs/{name}")
checkpoint = ModelCheckpoint(
    "models/{}.model".format(name, monitor="val_acc", verbose=1, save_best_only=True, mode='max'))

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

model.fit(
    x_train, y_train,
    epochs=3,
    batch_size=10,
    validation_split=0.1,
    callbacks=[tensorboard, checkpoint]
)
