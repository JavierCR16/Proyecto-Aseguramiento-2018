from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
from keras.models import model_from_json
import numpy as np
import os

def guardarModelo(filter_number, shape_tuple, str_activation, optim, loss_function, num_epochs, b_size):
    model = Sequential([
        Dense(filter_number, input_shape=shape_tuple),
        Activation(str_activation)
    ])

    model.compile(optimizer=optim,
              loss=loss_function,
              metrics=['accuracy'])

    data = np.random.random((1000, 100))
    labels = np.random.randint(2, size=(1000, 10))

    model.fit(data, labels, epochs = num_epochs, batch_size = b_size)
    
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights("model.h5")
    
def cargarModelo():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
 
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    score = loaded_model.evaluate(X, Y, verbose=0)
    # print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    