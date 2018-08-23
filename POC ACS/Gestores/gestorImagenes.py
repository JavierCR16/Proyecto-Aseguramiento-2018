'''
Created on Aug 19, 2018

@author: Javier
'''

## \package Gestores
#  Contiene todas las funciones asociadas al manejo de imagenes utilizando las librerias numpy y PIL
#
from PIL import Image
import numpy as np

## Descripcion de la funcion guardarImagen
#
#  Se encarga de guardar una imagen en el directorio de salida especificado
#  \param nombreArchivo Es el nombre de la imagen a buscar en la carpeta static
#  \param directorioArchivo Contiene el directorio de salida asi como el nombre de la imagen a guardar
#  \return Nada
def guardarImagen(nombreArchivo,directorioArchivo):
   imagenNueva= Image.fromarray(np.asarray(Image.open(nombreArchivo)))  
   imagenNueva.save(directorioArchivo)