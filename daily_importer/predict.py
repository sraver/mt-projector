import sys
import numpy as np
from tensorflow.keras.models import load_model
from src.Persistence.Database import Database
from src.Repositories.RawDataRepository import RawDataRepository
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from src.Preprocess.Sampler import Sampler

if len(sys.argv) < 6:
    print("Missing arguments!")
    exit()

pair = sys.argv[1]
timeframe = sys.argv[2]
from_date = sys.argv[3]
to_date = sys.argv[4]
name = sys.argv[5]

# Load raw data

raw_candles_repository = RawDataRepository(Database())
df = raw_candles_repository.get(pair, timeframe, from_date, to_date)

# Create samples

sampler = Sampler()

x_test, y_test = sampler.sample(timeframe, df)

y_test_original = y_test

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

print(f"x_train shape: {x_test.shape}")

# Predict

model = load_model(f"models/{name}.model")

y_pred = model.predict(x_test, batch_size=10)
y_pred_rounded = np.argmax(y_pred, axis=-1)

cm = confusion_matrix(y_test_original, y_pred_rounded)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1, 2])

disp.plot(cmap=plt.cm.get_cmap('Blues'))
plt.show()
