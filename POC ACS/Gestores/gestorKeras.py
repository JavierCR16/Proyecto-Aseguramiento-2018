from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
import numpy as np

def cargarModelo(data, labels, num_epochs, b_size):
    model = Sequential([
        Dense(32, input_shape=(100,)),
        Activation('relu')
    ])

    model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

    # data = np.random.random((1000, 100))
    # labels = np.random.randint(2, size=(1000, 10))

    model.fit(data, labels, epochs = num_epochs, batch_size = b_size)
    
def guardarModelo():
    return 0
    