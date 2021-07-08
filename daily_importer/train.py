import numpy as np
import time
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

pair = 'BTCUSD'
timeframe = 15

NAME = f"{pair}_{timeframe}_{time.time()}"

create_sequences = True

if create_sequences:
    db = Database()
    raw_candles_repository = RawDataRepository(db)

    # Load raw data

    df = raw_candles_repository.get(pair, timeframe, '2019-01-01', '2021-01-01')

    # sampler = BalancedSampler(Sampler())  # 11961
    sampler = Sampler()  # 63264

    x_train, y_train = sampler.sample(timeframe, df)

    np.save(f"samples/x_{NAME}.npy", x_train)
    np.save(f"samples/y_{NAME}.npy", y_train)

else:
    x_train = np.load(f"samples/x_{NAME}.npy")
    y_train = np.load(f"samples/y_{NAME}.npy")

y_train = to_categorical(y_train, 3)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

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
    optimizer=Adam(lr=1e-05),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

tensorboard = TensorBoard(log_dir=f"logs/{NAME}")

filepath = "RNN_Final-{epoch:02d}"
checkpoint = ModelCheckpoint(
    "models/{}.model".format(filepath, monitor="val_acc", verbose=1, save_best_only=True, mode='max'))

model.fit(
    x_train, y_train,
    epochs=3,
    batch_size=1000,
    validation_split=0.1,
    callbacks=[tensorboard, checkpoint]
)
