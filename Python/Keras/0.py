import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Activation,Convolution2D,MaxPooling2D,Flatten
from keras.optimizers import Adam

#CNN神经网络

def a():
    (X,Y),(X_t,Y_t)=mnist.load_data()
    X=X.reshape(-1,1,28,28)
    X_t=X_t.reshape(-1,1,28,28)
    Y=np_utils.to_categorical(Y,num_classes=10)
    Y_t=np_utils.to_categorical(Y_t,num_classes=10)

    model = Sequential()

    model.add(Convolution2D(filters=56, kernel_size=(7,7),
                            padding='same', input_shape=(1, 28, 28)))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
    model.add(Convolution2D(filters=56, kernel_size=(7,7),
                            padding='same'))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))

    model.add(Dense(10))
    model.add(Activation('softmax'))

    O=Adam(lr=1e-4)
    model.compile(optimizer=O,loss='categorical_crossentropy',metrics=["accuracy"])

    print("---------------------------------")
    model.fit(X,Y,epochs=2,batch_size=64)
    print("---------------------------------")
    Los,Acc=model.evaluate(X_t,Y_t)
    print ('\nLoss:\t',Los)
    print ('Acc :\t',Acc)
a()
