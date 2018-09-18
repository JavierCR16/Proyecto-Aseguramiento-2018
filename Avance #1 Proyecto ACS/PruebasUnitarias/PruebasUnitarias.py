'''
Created on Sep 13, 2018

@author: Javier
'''
import unittest
import os
from Gestores.GestorImagenes import *



class SimpleTestCase(unittest.TestCase):
    directorioImagenes = "C:/Users/Javier/Desktop/Aseguramiento de la Calidad del Software/Material Dropbox/Proyectos/datasets/Batch"
    gestorImagenes = GestorImagenes()
    tuplaInformacionImagenes = gestorImagenes.obtenerImagenes(directorioImagenes,'../static/')
    
    def test_directorioExistente(self):
        self.assertTrue(isinstance(self.tuplaInformacionImagenes,tuple), "Directorio No Existe")
    
    def test_archivosValidos(self):
        self.assertTrue(isinstance(self.tuplaInformacionImagenes,tuple), "Archivos no corresponden a un formato valido de Imagen")
        
    def test_valoresDevueltos(self):
        
        self.assertTrue(isinstance(self.tuplaInformacionImagenes[0],list),"Valor no corresponde a una lista (1)")
        self.assertTrue(isinstance(self.tuplaInformacionImagenes[1],list),"Valor no corresponde a una lista (2)")
        
    def test_imagenesProcesadas(self):
        cantidadImagenes = len([name for name in os.listdir(self.directorioImagenes)])

        self.assertTrue(len(self.tuplaInformacionImagenes[0]) == cantidadImagenes,"La cantidad de imagenes del directorio seleccionado no corresponde con la cantidad de elementos de salida (1)")
        self.assertTrue(len(self.tuplaInformacionImagenes[1]) == cantidadImagenes,"La cantidad de imagenes del directorio seleccionado no corresponde con la cantidad de elementos de salida (2)")
        
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()