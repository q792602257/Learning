from __future__ import print_function
import numpy as np
import keras
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten, Dropout
from keras.optimizers import Adam,RMSprop

#CNN 卷积神经网络
def cnn():
    (X,Y),(X_t,Y_t)=mnist.load_data()
    X = X.reshape(-1, 1, 28, 28).astype('float32') / 255
    X_t = X_t.reshape(-1, 1, 28, 28).astype('float32') / 255
    Y = np_utils.to_categorical(Y, num_classes=10)
    Y_t=np_utils.to_categorical(Y_t,num_classes=10)

    model = Sequential()

    model.add(Convolution2D(filters=56, kernel_size=(7,7),
                            padding='same', input_shape=(1, 28, 28),
                            activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

    model.add(Convolution2D(filters=56, kernel_size=(7,7),
                            padding='same',
                            activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

    model.add(Flatten())
    model.add(Dense(1024, activation="relu"))
    model.add(Dense(10, activation='softmax'))
    model.summary()

    O=Adam(lr=1e-4)
    model.compile(optimizer=O,
                loss='categorical_crossentropy',
                metrics=["accuracy"])

    print("---------------------------------")
    model.fit(X,Y,epochs=2,batch_size=64)
    print("---------------------------------")
    Los,Acc=model.evaluate(X_t,Y_t)
    print ('\nLoss:\t',Los)
    print ('Acc :\t',Acc)
    model.save("cnn.h5")

# DNN 深度神经网络
def dnn():
    (X, Y), (X_t, Y_t) = mnist.load_data()

    X = X.reshape(-1, 1, 28, 28).astype('float32') / 255
    X_t = X_t.reshape(-1, 1, 28, 28).astype('float32') / 255

    Y = keras.utils.to_categorical(Y, num_classes=10)
    Y_t = keras.utils.to_categorical(Y_t, num_classes=10)

    model = Sequential()
    model.add(Dense(1024, activation='relu', input_shape=(784,)))
    model.add(Dropout(0.01))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.01))
    model.add(Dense(10, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                optimizer=RMSprop(),
                metrics=['accuracy'])

    history = model.fit(X, Y,
                        batch_size=64,
                        epochs=2)
    score = model.evaluate(X_t, Y_t, verbose=0)
    print('Loss:\t', score[0])
    print('Acc :\t', score[1])

# cnn()
# dnn()
model = load_model("cnn.h5")
model.summary()
(X, Y), (X_t, Y_t) = mnist.load_data()
X = X.reshape(-1, 1, 28, 28).astype('float32') / 255
X_t = X_t.reshape(-1, 1, 28, 28).astype('float32') / 255

Y = keras.utils.to_categorical(Y, num_classes=10)
Y_t = keras.utils.to_categorical(Y_t, num_classes=10)
O = Adam(lr=1e-4)
model.compile(optimizer=O,
                loss='categorical_crossentropy',
                metrics=["accuracy"])
print("---------------------------------")
model.fit(X, Y, epochs=2, batch_size=64)
print("---------------------------------")
Los, Acc = model.evaluate(X_t, Y_t)
print('\nLoss:\t', Los)
print('Acc :\t', Acc)
model.save("cnn.h5")
