import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense

from src.Persistence.Database import Database
from src.Repositories.NormalizedCandlesRepository import NormalizedCandlesRepository
from src.Repositories.RawCandlesRepository import RawCandlesRepository
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler

pair = 'ETHUSD'
timeframe = 15

db = Database()
raw_candles_repository = RawCandlesRepository(db)
normal_candles_repository = NormalizedCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

# Filter data

arr_raw_candles = raw_candles.array()

prices = []
rsi = []
ema = []

for row in arr_raw_candles:
    prices.append(row.close())
    rsi.append(row.rsi())
    ema.append(row.ema50())

prices = np.array(prices)
rsi = np.array(rsi)
ema = np.array(ema)

# Normalize data

scaler_prices = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler_prices.fit_transform(prices.reshape(-1, 1))
scaler_rsi = MinMaxScaler(feature_range=(0, 1))
scaled_rsi = scaler_rsi.fit_transform(rsi.reshape(-1, 1))
scaler_ema = MinMaxScaler(feature_range=(0, 1))
scaled_ema = scaler_ema.fit_transform(ema.reshape(-1, 1))

scaled_data = np.concatenate([scaled_prices, scaled_rsi, scaled_ema], axis=1)

# Split to samples

batch_size = 10
delay_size = 4
price_increment = 0.06
set_size = len(arr_raw_candles)

x_train, y_train = [], []

for i in range(batch_size, set_size):
    from_index = i - batch_size
    to_index = i
    target_index = to_index + delay_size
    if target_index >= set_size:
        break

    first_element = arr_raw_candles[from_index]
    last_element = arr_raw_candles[to_index]
    target_element = arr_raw_candles[target_index]

    # Check target validity
    direction = 0
    if last_element.close() < target_element.close():
        direction = 1
    else:
        direction = -1

    x_train.append(scaled_data[from_index:to_index].reshape(1, -1)[0])
    y_train.append([scaled_data[target_index:target_index+1][0][0]])

x_train = np.array(x_train)
y_train = np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))

print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")

print("y train length: ", len(y_train))
print("Features size: ", len(x_train[0]))

# Create the model

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

'''


model.add(Dense(300, input_shape=(x_train.shape[1],), activation='relu'))
model.add(Dense(600, activation='relu'))
model.add(Dense(1, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
'''


model.fit(x_train, y_train, epochs=5, batch_size=32)
print(f"x_train shape: {x_train.shape} - y_train shape: {y_train.shape}")
