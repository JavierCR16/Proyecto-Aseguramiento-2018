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
from Gestores import gestor_etiquetado_coloreado
from Gestores.gestor_etiquetado_coloreado import pintar_coordenadas,\
    generar_centroides_celulas
import time

class GestorImagenes:
    """
    Docstring
    """

    def __init__(self):
        self.lista_nombres = []
        self.lista_preds = []
        self.lista_etiq = []
        self.cant_celulas_preds = []
        self.coordenadas_celulas = []
        self.centroides = []
        self.tiempos_lista = []

    @staticmethod
    def guardar_en_segmentacion(imagen, numero_imagen, path_test ):
        """
        Docstring
        """
        imagen.save(path_test + str(numero_imagen) + '.png')
    
    def formatear_tiempos(self):

        if(self.tiempos_lista[1]>60):
            tiempo_tmp = self.tiempos_lista[1] /60
            self.tiempos_lista[1] = str(round(tiempo_tmp,2))+" min"
        else:
            self.tiempos_lista[1] = str(round(self.tiempos_lista[1],2))+" s"
  
        index = 0
        for tiempo_imagen in self.tiempos_lista[0]:
            if(self.tiempos_lista[0][index] > 60):
                tiempo_tmp = self.tiempos_lista[0][index] /60
                self.tiempos_lista[0][index] = str(round(tiempo_tmp,2))+" min"
            else:
                self.tiempos_lista[0][index] = str(round(self.tiempos_lista[0][index],2))+" s"
            
            index += 1
            
    
    @staticmethod    
    def convertir_imagen(path_imagen_a_convertir):
        imagen_tmp = Image.open(path_imagen_a_convertir)
        imagen_tmp = imagen_tmp.convert('RGB')
        imagen_tmp.save(path_imagen_a_convertir)

    def obtener_imagenes(self, directorio_imagenes,
                         directorio_temporal='static/', path_test = '../Avance #3 Proyecto ACS/SegmentacionCelulas/raw/hoechst/test/'):
        """
        Docstring
        """
        num_img = 1
        try:
            for file in os.listdir(directorio_imagenes):
                path_imagen = directorio_imagenes+"/"+file
                imagen_nueva = Image.open(path_imagen)
                self.lista_nombres.append(str(num_img)+'.png')
                imagen_nueva.save(directorio_temporal+str(num_img)+'.png')
                GestorImagenes.guardar_en_segmentacion(imagen_nueva, num_img, path_test)
                num_img += 1
                
            self.lista_nombres = sorted(self.lista_nombres)
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
            
        self.lista_preds = sorted(self.lista_preds)
        return self.lista_preds
    
    def obtener_nombre_etiq(self,directorio_etiq):
        
        for file in os.listdir(directorio_etiq):
            self.lista_etiq.append(file)
            
        self.lista_etiq = sorted(self.lista_etiq)
        return self.lista_etiq
    
    def eliminar_directorios(self,tipo):
        path_preds = '../Avance #3 Proyecto ACS/SegmentacionCelulas/preds' if tipo == 0 else '../SegmentacionCelulas/preds'
        path_test = '../Avance #3 Proyecto ACS/SegmentacionCelulas/raw/hoechst/test/' if tipo == 0 else '../SegmentacionCelulas/raw/hoechst/test/'
        path_resultados = '../Avance #3 Proyecto ACS/SegmentacionCelulas/resultados/' if tipo == 0 else '../SegmentacionCelulas/resultados/'
        path_coloreadas = '../Avance #3 Proyecto ACS/SegmentacionCelulas/predsColoreadasEtiquetadas/' if tipo == 0 else '../SegmentacionCelulas/predsColoreadasEtiquetadas/'
        path_csv = '../Avance #3 Proyecto ACS/CSV/' if tipo == 0 else '../CSV/'
        path_static = "static/" if tipo == 0 else '../static/'
        static_files = os.listdir(path_static)
        
        if os.path.exists(path_preds):
            shutil.rmtree(path_preds)
            
        if os.path.exists(path_test):
            shutil.rmtree(path_test)
            os.makedirs(path_test)
        
        if os.path.exists(path_resultados):
            shutil.rmtree(path_resultados)
            os.makedirs(path_resultados)
            
        if os.path.exists(path_coloreadas):
            shutil.rmtree(path_coloreadas)
            os.makedirs(path_coloreadas)
            
        if os.path.exists(path_csv):
            shutil.rmtree(path_csv)
            os.makedirs(path_csv)
            
        for file in static_files:
            if file.endswith(".png"):
                os.remove(os.path.join(path_static,file))
        self.lista_nombres.clear()
        self.lista_preds.clear()
                
    def guardar_en_archivos(self):
        self.lista_nombres = sorted(self.lista_nombres)
        self.lista_preds = sorted(self.lista_preds)
        static_path = 'static/'
        path_resultados = '../Avance #3 Proyecto ACS/SegmentacionCelulas/resultados/'
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
    
    def colorear_etiquetar_imagenes(self,lista_tiempos):
        path_coloreadas = '../Avance #3 Proyecto ACS/SegmentacionCelulas/predsColoreadasEtiquetadas/'
        path_static = 'static/'
        
        for i in range (0, len(self.lista_preds)):
            tiempo_inicio = time.time()
            
            imagen_procesar = path_static + self.lista_preds[i]
            lista_celulas = gestor_etiquetado_coloreado.obtener_coordenadas_celulas(imagen_procesar)
            lista_minimos_maximos = gestor_etiquetado_coloreado.obtener_minimos_maximos(lista_celulas)
            centroides = gestor_etiquetado_coloreado.generar_centroides_celulas(lista_minimos_maximos, imagen_procesar)
            
            pintar_coordenadas(lista_celulas,imagen_procesar,path_coloreadas,path_static,self.lista_nombres[i].split('.')[0],centroides)
            self.cant_celulas_preds.append(len(lista_celulas))
            self.coordenadas_celulas.append([lista_celulas])
            self.centroides.append(centroides)
            
            tiempo_duracion = time.time()- tiempo_inicio
            lista_tiempos[0][i]+= tiempo_duracion #Accede a los tiempos de las imagenes
            lista_tiempos[1]+= tiempo_duracion
            