from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

from src.Model import Model


class ModelBuilder:
    BATCH_SIZE = 2
    EPOCHS = 3

    @staticmethod
    def build(x, y, name):
        model = Sequential()

        model.add(LSTM(units=64, return_sequences=True, input_shape=x.shape[1:]))
        model.add(Dropout(0.2))
        model.add(LSTM(units=64, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=32))
        model.add(Dropout(0.2))
        model.add(Dense(3, activation='softmax'))

        model.compile(
            optimizer=Adam(learning_rate=1e-06),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        tensorboard = TensorBoard(log_dir=f"logs/{name}")
        checkpoint = ModelCheckpoint(
            "models/{}.model".format(name, monitor="val_acc", verbose=1, save_best_only=True, mode='max')
        )

        model.fit(
            x, y,
            epochs=ModelBuilder.EPOCHS,
            batch_size=ModelBuilder.BATCH_SIZE,
            validation_split=0.1,
            callbacks=[tensorboard, checkpoint]
        )

        return Model(model, ModelBuilder.BATCH_SIZE)

    @staticmethod
    def load(name):
        model = load_model(f"models/{name}.model")
        return Model(model, ModelBuilder.BATCH_SIZE)
