import numpy as np, pandas as pd, time
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

from src.Candles.RawToNormalized import RawToNormalized
from src.Persistence.Database import Database
from src.Repositories.RawCandlesRepository import RawCandlesRepository
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

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

x_test, y_test = [], []

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

    x_test.append(sequence_array)
    y_test.append(direction)

x_test = np.array(x_test)
y_test = np.array(y_test)

x_test, y_test = shuffle(x_test, y_test)

y_test_original = y_test

y_test = to_categorical(y_test, 3)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

print(f"x_train shape: {x_test.shape} - y_train shape: {y_test.shape}")

# Predict

model = load_model("models/BTCUSD_15.mdl")

y_pred = model.predict(x_test)
y_pred_rounded = np.argmax(y_pred, axis=-1)
'''
print(y_test)
print(y_pred)
print(pd.DataFrame(y_test).value_counts())
print(pd.DataFrame(y_pred_rounded).value_counts())

con_mat = tf.math.confusion_matrix(labels=y_test_original, predictions=y_pred_rounded).numpy()
'''

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test_original, y_pred_rounded)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0,1,2])

disp.plot(cmap=plt.cm.get_cmap('Blues'))
plt.show()