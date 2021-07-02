import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

from src.Persistence.Database import Database
from src.Repositories.RawDataRepository import RawDataRepository
from sklearn.utils import shuffle

from src.Preprocess.Sampler import Sampler

pair = 'BTCUSD'
timeframe = 15

# Load raw data

db = Database()
raw_candles_repository = RawDataRepository(db)
df = raw_candles_repository.get(pair, timeframe)

# Create samples

sampler = Sampler()
x_test, y_test = sampler.sample(timeframe, df)

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