'''
Created on Sep 9, 2018

@author: Javier
'''
from PIL import Image
import numpy as np
import os

class GestorImagenes:
    def __init__(self):
        self.listaImagenes = []
        self.listaNombres = []

    def obtenerImagenes(self,directorioImagenes, directorioTemporal = 'static/'):
        try:
            for file in os.listdir(directorioImagenes):
                pathImagen = directorioImagenes +"/"+file
                imagenNueva= Image.fromarray(np.asarray(Image.open(pathImagen))) #nombreArchivo,extension = os.path.splitext(file)
                
                self.listaImagenes.append(imagenNueva)
                self.listaNombres.append(file)
                imagenNueva.save(directorioTemporal+file)#nombreArchivo+extension) #Se guardan del lado del cliente para mostrarlas a pantalla
               
            return self.listaImagenes, self.listaNombres
        except Exception as e:
            return False