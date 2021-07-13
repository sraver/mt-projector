import time
import subprocess

interpreter = 'python3.9'

pair = 'BTCUSD'
timeframe = 60

train_from, train_to = '2020-01-01', '2020-12-31'
test_from, test_to = '2021-01-01', '2021-07-01'

batch_name = f"{pair}_{timeframe}_{time.time()}"

subprocess.call(f"{interpreter} train.py {pair} {timeframe} {train_from} {train_to} {batch_name}", shell=True)

subprocess.call(f"{interpreter} predict.py {pair} {timeframe} {test_from} {test_to} {batch_name}", shell=True)
