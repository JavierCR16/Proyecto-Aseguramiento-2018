'''
Created on Sep 9, 2018

@author: Javier
'''
import os
import traceback
from PIL import Image
import numpy as np


class GestorImagenes:
    """
    Docstring
    """

    def __init__(self):
        self.lista_nombres = []
        self.lista_preds = []

    @staticmethod
    def guardar_en_segmentacion(imagen, numero_imagen, path_test ):
        """
        Docstring
        """
        imagen.save(path_test + str(numero_imagen) + '.png')

    def obtener_imagenes(self, directorio_imagenes,
                         directorio_temporal='static/', path_test = '../Avance #2 Proyecto ACS/SegmentacionCelulas/raw/hoechst/test/'):
        """
        Docstring
        """
        num_img = 1
        try:
            for file in os.listdir(directorio_imagenes):
                path_imagen = directorio_imagenes+"/"+file
                arreglo_imagen = np.asarray(Image.open(path_imagen))
                imagen_nueva = Image.fromarray(arreglo_imagen)
                self.lista_nombres.append(str(num_img)+'.png')
                imagen_nueva.save(directorio_temporal+str(num_img)+'.png')
                GestorImagenes.guardar_en_segmentacion(imagen_nueva, num_img, path_test)
                num_img += 1

            return self.lista_nombres
        except Exception:
            traceback.print_exc()
            return False

    def obtener_nombre_preds(self, directorio_preds):
        """
        Docstring
        """
        for file in os.listdir(directorio_preds):
            self.lista_preds.append(file)

        return self.lista_preds
