'''
Created on Aug 23, 2018

@author: Javier
'''
import unittest
from Gestores import gestorCSV,gestorImagenes
from Gestores.gestorCSV import registroObjetos
from Gestores.gestorImagenes import  guardarImagen

class SimpleTestCase(unittest.TestCase):
    
    def test_existePath(self):
        listaDatos = [{'identificacion':'1', 'centroide':'234','area': '467'}]
        pathFalso = 'ProyectoAseguramiento/CSV/listaObjetos.csv'
        self.assertFalse(registroObjetos(listaDatos, pathFalso))
        
    
    def test_DatosValidosCSV(self):
        datosValidos = ['identificacion','centroide','area']
        listaDatos = [{datosValidos[0].lower():'1', datosValidos[1].lower():'234',datosValidos[2].lower(): '467'},
                      {datosValidos[0].lower():'2', datosValidos[1].lower():'1000',datosValidos[2].lower(): '4967'},
                      {datosValidos[0].lower():'3', datosValidos[1].lower():'678',datosValidos[2].lower(): '492'}]

        self.assertTrue(registroObjetos(listaDatos,'../CSV/listaObjetos.csv'))
        
    
    def test_imagenyDirectorioInexistente(self):#,fuente,archivo
        nombreArchivo= "../static/Whales-Tail-Uvita.jpg"
        outputDirectory="../static/hola.jpg"
        self.assertTrue(guardarImagen(nombreArchivo,outputDirectory))
        
 
if __name__ == "__main__":
        unittest.main() 