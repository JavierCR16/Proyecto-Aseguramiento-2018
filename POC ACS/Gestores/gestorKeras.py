from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
from keras.models import model_from_json
import numpy as np
import os

def guardarModelo(model_name, filter_number, shape_tuple, str_activation, optim, loss_function, num_epochs, b_size):
    try:
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
    
        model_json = model.to_json()
        str_name = model_name + ".json"
        with open(str_name, "w") as json_file:
            json_file.write(model_json)

        str_name = model_name + ".h5"
        model.save_weights(str_name)
        return True
    except:
        return False
    
def cargarModelo(name):
    try:
        model_name = name + ".json"
        json_file = open(model_name, 'r')
        modelo_cargado_json = json_file.read()
        json_file.close()
        modelo_cargado = model_from_json(modelo_cargado_json)

        model_name = name + ".h5"
        modelo_cargado.load_weights(model_name)
        print("Modelo cargado")
     
        modelo_cargado.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        
        data = np.random.random((1000, 100))
        labels = np.random.randint(2, size=(1000, 10))
    
        score = modelo_cargado.evaluate(data, labels, verbose=0)
        print("%s: %.2f%%" % (modelo_cargado.metrics_names[1], score[1]*100))
        return True
    except:
        return False