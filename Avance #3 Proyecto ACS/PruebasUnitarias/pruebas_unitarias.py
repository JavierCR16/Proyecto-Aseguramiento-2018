'''
Created on Sep 13, 2018

@author: Javier
'''
import unittest
import os
from Gestores.gestor_imagenes import GestorImagenes
from SegmentacionCelulas import unet_CellSegmentation as segmentador


class SimpleTestCase(unittest.TestCase):
    directorioImagenes = "C:/Users/Javier/Desktop/Aseguramiento de la Calidad del Software/Material Dropbox/Proyectos/datasets/Batch"
    gestorImagenes = GestorImagenes()
    listaImagenes = gestorImagenes.obtener_imagenes(directorioImagenes,
                                                    '../static/','../SegmentacionCelulas/raw/hoechst/test/')
    segmentador.image_path = '../SegmentacionCelulas/raw/hoechst/test/*.png'
    segmentador.weights_path = '../SegmentacionCelulas/weights/pre_0_3_5.h5'
    segmentador.pred_dir = '../SegmentacionCelulas/preds/'
    segmentador.file_path = '../SegmentacionCelulas/imgs_mask_predict.npy'
    segmentador.static_path = '../static/'
    
    segmentador.predict()

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
        
    def test_existen_pesos(self):
        existe_pesos = os.path.exists('../SegmentacionCelulas/weights/pre_0_3_5.h5')
        self.assertTrue(existe_pesos, "No existe un archivo de pesos valido")    
        
    def test_carga_datos(self):
        dir_test = '../SegmentacionCelulas/raw/hoechst/test'
        cant_imagenes = len([name for
                                 name in os.listdir(dir_test)])
        valores = segmentador.load_test_data(segmentador.image_path)
        self.assertTrue(len(valores[0]) == cant_imagenes, "No todas las imagenes fueron procesadas")
        
    def test_archivodatos_creado(self):

        existe_archivo = os.path.exists('../SegmentacionCelulas/imgs_mask_predict.npy')
        self.assertTrue(existe_archivo, "Archivo de Datos no fue creado")
     
    def test_predicciones_creadas(self):
        
        existe_predicciones = os.path.exists('../SegmentacionCelulas/preds/')
        self.assertTrue(existe_predicciones, "Predicciones no fueron creadas")
    

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
