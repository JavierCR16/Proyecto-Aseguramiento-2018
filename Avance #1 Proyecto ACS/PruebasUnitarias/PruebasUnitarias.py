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
    
    def test_archivosValidos(self):
        self.assertTrue(isinstance(self.tuplaInformacionImagenes,tuple))
        
    def test_valoresDevueltos(self):
        
        self.assertTrue(isinstance(self.tuplaInformacionImagenes[0],list))
        self.assertTrue(isinstance(self.tuplaInformacionImagenes[1],list))
        
    def test_imagenesProcesadas(self):
        cantidadImagenes = len([name for name in os.listdir(self.directorioImagenes)])

        self.assertTrue(len(self.tuplaInformacionImagenes[0]) == cantidadImagenes)
        self.assertTrue(len(self.tuplaInformacionImagenes[1]) == cantidadImagenes)
        
   
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()