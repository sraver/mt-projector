import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical

from src.Candles.RawToNormalized import RawToNormalized
from src.Persistence.Database import Database
from src.Repositories.RawCandlesRepository import RawCandlesRepository
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler

pair = 'BTCUSD'
timeframe = 15

db = Database()
raw_candles_repository = RawCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

converter = RawToNormalized(raw_candles)
normal_candles = converter.convert()

arr_normal_candles = normal_candles.array()

# Filter wanted data

times = []
closes = []
rsi = []
ema = []

for row in arr_normal_candles:
    times.append(row.date())
    closes.append(row.close())
    rsi.append(row.rsi())
    ema.append(row.ema50())

'''
times = np.array(times).reshape(-1, 1)
prices = np.array(prices)
rsi = np.array(rsi)
ema = np.array(ema)
'''

df = pd.DataFrame(
    {
        'time': times,
        'close': closes,
        'rsi': rsi,
        'ema': ema
    },
    columns=['time', 'close', 'rsi', 'ema']
) \
    .set_index('time')

# Normalize data

scaler_prices = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler_prices.fit_transform(df.close.values.reshape(-1, 1)).reshape(1, -1)[0]

scaler_ema = MinMaxScaler(feature_range=(0, 1))
scaled_ema = scaler_ema.fit_transform(df.ema.values.reshape(-1, 1)).reshape(1, -1)[0]

df.rsi /= 100

scaled_df = pd.DataFrame(
    {
        'time': times,
        'close': scaled_prices,
        'rsi': df.rsi.values,
        'ema': scaled_ema
    },
    columns=['time', 'close', 'rsi', 'ema']
) \
    .set_index('time')

# Generate samples

period_size = 60
delay_periods = 4
change_threshold = 0.01

collection_size = len(arr_normal_candles)

x_train, y_train = [], []

for i in range(period_size, collection_size):
    from_index = i - period_size
    to_index = i
    target_index = to_index + delay_periods
    if target_index >= collection_size:
        break

    # Check range completeness

    current_sequence = scaled_df[from_index:target_index]
    expected_range = pd.date_range(
        current_sequence.index[0],
        periods=period_size + delay_periods,
        freq=f"{timeframe}min"
    )

    range_has_gaps = expected_range[-1] != current_sequence.index[-1]

    if range_has_gaps:
        continue

    # Check target validity

    change = 0
    for index in range(to_index + 1, target_index + 1):
        change = change + arr_normal_candles[index].close()

    direction = 0
    if change > change_threshold:
        direction = 1
    elif change < change_threshold * -1:
        direction = 2

    sequence_array = current_sequence[:-delay_periods] \
        .to_numpy() \
        .reshape(1, -1)[0]

    x_train.append(sequence_array)
    y_train.append(direction)

x_train = np.array(x_train)
y_train = np.array(y_train)

y_train = to_categorical(y_train, 3)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
# y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

# Create the model

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1:])))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

'''

model.add(Dense(100, input_shape=(x_train.shape[1],), activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
'''

model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")
