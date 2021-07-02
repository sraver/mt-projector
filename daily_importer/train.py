import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical

from src.Persistence.Database import Database
from src.Repositories.RawDataRepository import RawDataRepository
from sklearn.utils import shuffle

from src.Preprocess.Sampler import Sampler

pair = 'BTCUSD'
timeframe = 15

create_sequences = True

if create_sequences:
    db = Database()
    raw_candles_repository = RawDataRepository(db)

    # Load raw data

    df = raw_candles_repository.get(pair, timeframe)

    sampler = Sampler()

    x_train, y_train = sampler.sample(timeframe, df)

    np.save(f"samples/x_{pair}_{timeframe}.npy", x_train)
    np.save(f"samples/y_{pair}_{timeframe}.npy", y_train)

else:
    x_train = np.load(f"samples/x_{pair}_{timeframe}.npy")
    y_train = np.load(f"samples/y_{pair}_{timeframe}.npy")

x_train, y_train = shuffle(x_train, y_train)

y_train = to_categorical(y_train, 3)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

# Create the model

model = Sequential()

model.add(LSTM(units=128, return_sequences=True, input_shape=x_train.shape[1:]))
model.add(Dropout(0.2))

model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=64))
model.add(Dropout(0.2))

model.add(Dense(3, activation='softmax'))

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=1, batch_size=3, validation_split=0.1)

model.save(f"models/{pair}_{timeframe}_2.mdl")
