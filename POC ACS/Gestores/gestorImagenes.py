'''
Created on Aug 19, 2018

@author: Javier
'''
from PIL import Image
import numpy as np

def guardarImagen(nombreArchivo,directorioArchivo):
  # imagenAbierta =  Image.open(nombreArchivo)
   #imagenArreglo = np.asarray(imagenAbierta)
   imagenNueva= Image.fromarray(np.asarray(Image.open(nombreArchivo)))     #(imagenArreglo)
   imagenNueva.save(directorioArchivo)#"../POC ACS/static/nuevaImagen.png")