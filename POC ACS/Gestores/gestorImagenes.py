'''
Created on Aug 19, 2018

@author: Javier
'''
from PIL import Image
import numpy as np

def guardarImagen(nombreArchivo,directorioArchivo):
   imagenNueva= Image.fromarray(np.asarray(Image.open(nombreArchivo)))  
   imagenNueva.save(directorioArchivo)