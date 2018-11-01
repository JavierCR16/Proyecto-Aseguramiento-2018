'''
Created on Sep 9, 2018

@author: Javier
'''
import os
import traceback
from PIL import Image
import numpy as np
from django.urls.conf import path
import shutil


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
    
    def eliminar_directorios(self):
        path_preds = '../Avance #2 Proyecto ACS/SegmentacionCelulas/preds'
        path_test = '../Avance #2 Proyecto ACS/SegmentacionCelulas/raw/hoechst/test/'
        path_resultados = '../Avance #2 Proyecto ACS/SegmentacionCelulas/resultados/'
        path_static = "static/"
        static_files = os.listdir(path_static)
        
        if os.path.exists(path_preds):
            shutil.rmtree(path_preds)
            
        if os.path.exists(path_test):
            shutil.rmtree(path_test)
            os.makedirs(path_test)
        
        if os.path.exists(path_resultados):
            shutil.rmtree(path_resultados)
            os.makedirs(path_resultados)
            
        for file in static_files:
            if file.endswith(".png"):
                os.remove(os.path.join(path_static,file))
        self.lista_nombres.clear()
        self.lista_preds.clear()
                
    def guardar_en_archivos(self):
        self.lista_nombres = sorted(self.lista_nombres)
        self.lista_preds = sorted(self.lista_preds)
        static_path = 'static/'
        path_resultados = '../Avance #2 Proyecto ACS/SegmentacionCelulas/resultados/'
        contador = 1
        
        for i in range (0, len(self.lista_nombres)):
            
            images = [Image.open(static_path+self.lista_preds[i])]
            size_pred = images[0].size
            
            original_resize = Image.open(static_path+self.lista_nombres[i])
            original_resize = original_resize.resize(size_pred,Image.ANTIALIAS) #Thumbnail mantiene el aspect ratio de la imagen
            original_resize.save(static_path+self.lista_nombres[i])
            
            images.insert(0,Image.open(static_path+self.lista_nombres[i]))
            
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)
            
            x_offset = 0
            imagen_nueva = Image.new('L',(total_width,max_height))
            for imagen in images:
                imagen_nueva.paste(imagen, (x_offset,0))
                x_offset += imagen.size[0]
            
            imagen_nueva.save(path_resultados+'resultado'+str(contador)+'.png')
            contador += 1
