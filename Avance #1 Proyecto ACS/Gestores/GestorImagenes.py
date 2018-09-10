'''
Created on Sep 9, 2018

@author: Javier
'''
from PIL import Image
import numpy as np
import os

def obtenerImagenes(directorioImagenes):
    listaImagenes = []
    listaNombres =  []
    for file in os.listdir(directorioImagenes):
        pathImagen = directorioImagenes +"/"+file
        imagenNueva= Image.fromarray(np.asarray(Image.open(pathImagen)))
        nombreArchivo,extension = os.path.splitext(file)
        listaImagenes.append(imagenNueva)
        listaNombres.append(file)
        imagenNueva.save('static/'+nombreArchivo+extension) #Se guardan del lado del cliente para mostrarlas a pantalla
        
    return listaImagenes,listaNombres
