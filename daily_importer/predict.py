import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from src.Persistence.Database import Database
from src.Repositories.RawDataRepository import RawDataRepository
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from src.Preprocess.Sampler import Sampler

pair = 'BTCUSD'
timeframe = 15

# Load raw data

db = Database()
raw_candles_repository = RawDataRepository(db)
df = raw_candles_repository.get(pair, timeframe, '2021-01-01', '2021-07-01')

# Create samples

sampler = Sampler()

x_test, y_test = sampler.sample(timeframe, df)

y_test_original = y_test

y_test = to_categorical(y_test, 3)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

print(f"x_train shape: {x_test.shape} - y_train shape: {y_test.shape}")

# Predict

model = load_model("models/BTCUSD_15_2.mdl")

y_pred = model.predict(x_test)
y_pred_rounded = np.argmax(y_pred, axis=-1)

cm = confusion_matrix(y_test_original, y_pred_rounded)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1, 2])

disp.plot(cmap=plt.cm.get_cmap('Blues'))
plt.show()
