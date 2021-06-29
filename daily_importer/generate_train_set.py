import numpy as np
from src.Candles.RawToNormalized import RawToNormalized
from src.Persistence.Database import Database
from src.Repositories.RawCandlesRepository import RawCandlesRepository
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPRegressor

pair = 'ETHUSD'
timeframe = 15

db = Database()
raw_candles_repository = RawCandlesRepository(db)

# Load raw data

raw_candles = raw_candles_repository.get(pair, timeframe)

# Convert to differentials

converter = RawToNormalized(raw_candles)
normal_candles = converter.convert()

arr_normal_candles = normal_candles.array()

batch_size = 10
delay_size = 4
price_increment = 0.06
set_size = len(arr_normal_candles)

print("Total rows: ", set_size)

X_set, Y_set = [], []

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
    variance = 0
    for index in range(to_index + 1, target_index + 1):
        diff = diff + arr_normal_candles[index].close()
        variance = diff / price_increment

    current_row = []
    for j in range(from_index, to_index):
        element = arr_normal_candles[j]
        current_row.append(element.month_of_year())
        current_row.append(element.day_of_week())
        current_row.append(element.hour())
        current_row.append(element.close())
        current_row.append(element.rsi())
        current_row.append(element.ema50())
        current_row.append(element.ema200())
        current_row.append(element.ema800())

    X_set.append(current_row)
    Y_set.append(variance)

X = np.array(X_set)
Y = np.array(Y_set)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

mlp = MLPRegressor(hidden_layer_sizes=(50, 50, 50), max_iter=1000)

print("Training")
mlp.fit(X_train, Y_train)

print("Predictions")
predict_train = mlp.predict(X_test)

print("Results")

mae = metrics.mean_absolute_error(Y_test, predict_train)
mse = metrics.mean_squared_error(Y_test, predict_train)
r2 = metrics.r2_score(Y_test, predict_train)

print("The model performance for testing set")
print("--------------------------------------")
print('MAE is {}'.format(mae))
print('MSE is {}'.format(mse))
print('R2 score is {}'.format(r2))

