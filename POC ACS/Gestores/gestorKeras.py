## \package Gestores
#  Modulo que contiene funciones de carga y guardado de modelos de aprendizaje, mediante el uso de la libreria Keras
#

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
from keras.models import model_from_json
import numpy as np
import os

## Descripcion de la funcion guardarModelo
#
#  Toma los parametros dados por el usuario, crea un modelo en base a ellos, y guarda tal modelo en un archivo .JSON
#  \param model_name Define el nombre del modelo, asi como los archivos
#  \param filter_number Numero de filtros utilizados por el modelo
#  \param shape_tuple Tupla de valores donde se define la forma
#  \param str_activation Define el modo de activacion del modelo (relu, sigmoid, softmax, etc.)
#  \param optim Describe el optimizador para compilar el modelo (usualmente rmsprop)
#  \param loss_function Define la funcion de perdida (binaria, multiple)
#  \param b_size Asigna los tamanos para los batches
#  \return Nada

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
    
## Descripcion de la funcion cargarModelo
#
#  En base a un nombre de archivo, busca el JSON del modelo junto con los pesos y los carga a memoria
#  \param model_name Indica el nombre del modelo, y por ende los archivos
#  \return Nada

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