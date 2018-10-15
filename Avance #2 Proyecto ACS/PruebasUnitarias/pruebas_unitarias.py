'''
Created on Sep 13, 2018

@author: Javier
'''
import unittest
import os
from Gestores.gestor_imagenes import GestorImagenes


class SimpleTestCase(unittest.TestCase):
    directorioImagenes = "C:/Users/Javier/Desktop/Aseguramiento de la Calidad del Software/Material Dropbox/Proyectos/datasets/Batch"
    gestorImagenes = GestorImagenes()
    listaImagenes = gestorImagenes.obtener_imagenes(directorioImagenes,
                                                    '../static/')

    def test_directorio_existente(self):
        self.assertTrue(isinstance(self.listaImagenes, list),
                        "Directorio No Existe")

    def test_archivos_validos(self):
        self.assertTrue(isinstance(self.listaImagenes, list),
                        "Archivos no corresponden a un formato de Imagen")

    def test_valores_devueltos(self):

        self.assertTrue(isinstance(self.listaImagenes, list),
                        "Valor no corresponde a una lista (1)")

    def test_imagenes_procesadas(self):
        cantidad_imagenes = len([name for
                                 name in os.listdir(self.directorioImagenes)])

        self.assertTrue(len(self.listaImagenes) == cantidad_imagenes,
                        "La cantidad de imagenes del directorio seleccionado no corresponde con la cantidad de elementos de salida (1)")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
