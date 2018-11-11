'''
Created on Sep 13, 2018

@author: Javier
'''
import unittest
import os
from PIL import Image
from Gestores.gestor_imagenes import GestorImagenes
from Gestores import gestor_coloreado
from Gestores import gestor_csv
from Gestores import gestor_etiquetado
from Gestores import gestor_imagenes
from SegmentacionCelulas import unet_CellSegmentation as segmentador
from wheel.signatures import assertTrue
from Modelos.ModeloObjeto import ObjetoImagen
from Gestores.gestor_csv import registroObjetos


class SimpleTestCase(unittest.TestCase):
    directorioImagenes = "C:/Users/Javier/Desktop/Aseguramiento de la Calidad del Software/Material Dropbox/Proyectos/datasets/Batch"
    directorioColoreadas = '../SegmentacionCelulas/predsColoreadasEtiquetadas/'
    gestorImagenes = GestorImagenes()
    gestorImagenes.eliminar_directorios(1)
    
    listaImagenes = gestorImagenes.obtener_imagenes(directorioImagenes,
                                                    '../static/','../SegmentacionCelulas/raw/hoechst/test/') 
    segmentador.image_path = '../SegmentacionCelulas/raw/hoechst/test/*.png'
    segmentador.weights_path = '../SegmentacionCelulas/weights/pre_0_3_5.h5'
    segmentador.pred_dir = '../SegmentacionCelulas/preds/'
    segmentador.file_path = '../SegmentacionCelulas/imgs_mask_predict.npy'
    segmentador.static_path = '../static/'
    
    segmentador.predict()
    
    lista_preds = gestorImagenes.obtener_nombre_preds('../SegmentacionCelulas/preds/')

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
        valores = segmentador.load_test_data(segmentador.image_path,[])
        self.assertTrue(len(valores[0]) == cant_imagenes, "No todas las imagenes fueron procesadas")
        
    def test_archivodatos_creado(self):

        existe_archivo = os.path.exists('../SegmentacionCelulas/imgs_mask_predict.npy')
        self.assertTrue(existe_archivo, "Archivo de Datos no fue creado")
     
    def test_predicciones_creadas(self):
        
        existe_predicciones = os.path.exists('../SegmentacionCelulas/preds/')
        self.assertTrue(existe_predicciones, "Predicciones no fueron creadas")
    
    #A PARTIR DE AQUI LAS PRUEBAS UNITARIAS DEL AVANCE #3
    
    def test_pixeles_celula(self):
        lista_celulas = gestor_coloreado.obtener_coordenadas_celulas('../static/'+self.lista_preds[0])
        self.assertTrue(isinstance(lista_celulas, list))
        self.assertTrue(isinstance(lista_celulas[0],list))
        
    
    def test_centroides_generados(self):
        lista_celulas = gestor_coloreado.obtener_coordenadas_celulas('../static/'+self.lista_preds[0])
        lista_tupla_ejes = gestor_coloreado.obtener_minimos_maximos(lista_celulas)
        lista_centros = gestor_coloreado.generar_centroides_celulas(lista_tupla_ejes, '../static/'+self.lista_preds[0])
        
        self.assertTrue(isinstance(lista_centros,list))
        self.assertTrue(isinstance(lista_centros[0], tuple))
          
    def test_generar_csv_dice(self):
        gestor_csv.calcular_precision_dice(self.lista_preds,1)
        
        self.assertTrue(os.path.exists('../CSV/datos_dice.csv'))
        
    def test_registro_objetos(self):
        objetos_stub = [ObjetoImagen(4,(35,50),500).__dict__, ObjetoImagen(5,(80,90),300).__dict__, ObjetoImagen(6,(90,100),800).__dict__]
        gestor_csv.registroObjetos(objetos_stub, "Stub", "../CSV/")
        
        self.assertTrue(os.path.exists("../CSV/objetos_celulasStub.csv"))
        
    def test_etiquetado(self):
        random_rgb_image = Image.new('RGB', (256,256))
        coordenadas_centroide = [(30,45),(100,40),(20,234),(70,100),(150,45),(90,20),(10,231),(60,60),(150,150),(100,100)]
        path_etiq = '../SegmentacionCelulas/predsColoreadasEtiquetadas/'
        gestor_etiquetado.etiquetar_imagen(random_rgb_image, coordenadas_centroide, '../static/', path_etiq, "Stub")
        
        self.assertTrue(os.path.exists(path_etiq + 'predColorEtiqStub.png'))
        
    #A PARTIR DE AQUI LAS PRUEBAS DE INTEGRACION del AVANCE #3
    
    def test_celulas_pintadas_etiquetadas(self):
        lista_celulas = gestor_coloreado.obtener_coordenadas_celulas('../static/'+self.lista_preds[0])
        lista_tupla_ejes = gestor_coloreado.obtener_minimos_maximos(lista_celulas)
        lista_centros = gestor_coloreado.generar_centroides_celulas(lista_tupla_ejes, '../static/'+self.lista_preds[0])
        
        imagen_color = gestor_coloreado.pintar_coordenadas(lista_celulas, '../static/'+self.lista_preds[0])
        
        gestor_etiquetado.etiquetar_imagen(imagen_color, lista_centros, '../static/', self.directorioColoreadas, "integradoEtiq")
        
        self.assertTrue(len(os.listdir(self.directorioColoreadas)) != 0)
    
    def test_generar_csv_objeto(self):
        lista_celulas = gestor_coloreado.obtener_coordenadas_celulas('../static/'+self.lista_preds[0])
        lista_tupla_ejes = gestor_coloreado.obtener_minimos_maximos(lista_celulas)
        lista_centros = gestor_coloreado.generar_centroides_celulas(lista_tupla_ejes, '../static/'+self.lista_preds[0])

        gestor_csv.procesar_informacion_celulas([[lista_celulas]], [lista_centros], self.listaImagenes, 1)
        
        self.assertTrue(os.path.exists('../CSV/objetos_celulas1.csv'))
        
    def test_general_colorear_etiquetar(self):
        self.gestorImagenes.lista_preds = self.gestorImagenes.lista_preds[:4]
        lista_tiempos = [[0 for x in range(4)],0]
        estado_retorno = self.gestorImagenes.colorear_etiquetar_imagenes(lista_tiempos, 1)
        
        self.assertTrue(estado_retorno)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
