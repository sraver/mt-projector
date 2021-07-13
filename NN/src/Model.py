import numpy as np
from tensorflow.python.keras import Sequential
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


class Model:

    def __init__(self, model: Sequential, batch_size):
        self.model = model
        self.batch_size = batch_size

    def predict(self, x):
        y_predicted = self.model.predict(x, self.batch_size)
        return y_predicted

    @staticmethod
    def plot_confusion_matrix(y_test, y_predicted):
        y_rounded = np.argmax(y_predicted, axis=-1)
        cm = confusion_matrix(y_test, y_rounded)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1, 2])
        disp.plot(cmap=plt.cm.get_cmap('Blues'))
        plt.show()
