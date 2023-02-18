class dnn_model():
    def __init__(self,
                 csv='TrainingSample_XY_3.csv'):
        self.csv = csv
        self.x, self.y = self.preprocess()
        print(self.csv)

    def preprocess(self):
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import MinMaxScaler
        df = pd.read_csv(self.csv)
        xy = df.values
        x = xy[:, 1:-1]
        y = xy[:, -1]
        x = np.append(x[:, 0:2], x[:, -5:], axis=1)
        x = MinMaxScaler().fit(x).transform(x)

        return x, y

    def model_regression(self, x, y,
                         optimizer, loss, validation_split, epochs):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        # create model
        model = Sequential()

        # get number of columns in training data
        n_cols = x.shape[1]

        # add model layers
        model.add(Dense(50, activation='relu', input_shape=(n_cols,)))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(1))

        # model.compile(optimizer='adam', loss='mean_squared_error')
        model.compile(optimizer=optimizer, loss=loss)

        # from keras.callbacks import EarlyStopping
        # set early stopping monitor so the model stops training when it won't improve anymore
        # early_stopping_monitor = EarlyStopping(patience=3)
        # train model
        # model.fit(x, y, validation_split=0.2, epochs=50, callbacks=[early_stopping_monitor])
        hist_regression = model.fit(x, y, validation_split=validation_split, epochs=epochs)
        self.model_reg = model
        return hist_regression

    def model_classification(self, x, y,
                             optimizer, loss, metrics, validation_split, epochs):
        y_discrete = y.astype(int)
        from keras.utils import to_categorical
        # one-hot encode target column
        y_discrete = to_categorical(y_discrete)

        from keras.models import Sequential
        from keras.layers import Dense
        model_2 = Sequential()

        # get number of columns in training data
        n_cols_2 = x.shape[1]

        # add layers to model
        model_2.add(Dense(64, activation='relu', input_shape=(n_cols_2,)))
        model_2.add(Dense(32, activation='relu'))
        # model_2.add(Dense(16, activation='relu'))
        model_2.add(Dense(y_discrete.shape[1], activation='softmax'))

        # compile model using accuracy to measure model performance
        model_2.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        hist_classification = model_2.fit(x, y_discrete, epochs=epochs, validation_split=validation_split)
        self.model_class = model_2
        return hist_classification

    def plot_hist_regression(self, hist):
        from matplotlib import pyplot as plt
        # history = model1.fit(train_x, train_y,validation_split = 0.1, epochs=50, batch_size=4)
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper right')
        plt.show()

    def plot_hist_classification(self, hist):
        from matplotlib import pyplot as plt
        plt.plot(hist.history['accuracy'])
        plt.plot(hist.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='lower right')
        plt.show()

    def run_regression(self,
                       optimizer='adam',
                       loss='mean_absolute_error',
                       validation_split=0.2,
                       epochs=200):
        hist_regression = self.model_regression(self.x, self.y,
                                                optimizer, loss, validation_split, epochs)
        #self.plot_hist_regression(hist_regression)

    def run_classification(self,
                           optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'],
                           validation_split=0.2,
                           epochs=500):
        hist_class = self.model_classification(self.x, self.y,
                                               optimizer, loss, metrics, validation_split, epochs)
        self.plot_hist_classification(hist_class)