'''
Created on Aug 19, 2018

@author: Javier
'''

## \package Gestores
#  Contiene todas las funciones asociadas al manejo de archivos de extension CSV utilizando la libreria PANDAS
#

import pandas
from collections import namedtuple
from Modelos.ModeloObjeto import ObjetoImagen
from PIL import Image
import numpy as np


## Descripcion de la funcion registroObjetos
#
#  Se encarga de agrupar los datos, que provienen en diccionarios, en tres categorias las cuales seran cargadas en un archivo CSV
#  \param listaObjetos Es una lista de diccionarios y cada diccionario contiene los atributos de area, centroide e identificacion
#  \param directorio Es el directorio de salida en donde se va a generar el CSV
#  \return Nada
def registroObjetos(listaObjetos,contador, path_csv): #ObjetoImagen(__numero,__centroide,__area).__dict__
    try:
        listaIdentificacion= [d["identificacion"] for d in listaObjetos ]
        listaCentroide= [d["centroide"] for d in listaObjetos]
        listaArea = [d["area"] for d in listaObjetos]
        diccionario = {'Identificacion':listaIdentificacion,'Centroide': listaCentroide,'Area': listaArea}
        
        datos = pandas.DataFrame(diccionario)
        datos.to_csv(path_csv + 'objetos_celulas' +str(contador)+'.csv')
        return True
    except:
        return False
    
def procesar_informacion_celulas(lista_archivos_celulas, lista_centroides,identificadores_archivos, tipo):
    path_csv = '../Avance #3 Proyecto ACS/CSV/' if tipo == 0 else '../CSV/'
    
    identificadores_archivos = sorted(identificadores_archivos)
    listaObjetos = []
    identificador = 1
    contador = 0
    index_centroide = 0
    for archivo_celulas in lista_archivos_celulas:
        for lista_celulas in archivo_celulas:
            for celula in lista_celulas:
                centroide = lista_centroides[contador][index_centroide]
                listaObjetos.append(ObjetoImagen(identificador,centroide,len(celula)).__dict__)
                identificador += 1
                index_centroide += 1
        
        registroObjetos(listaObjetos, identificadores_archivos[contador].split('.')[0],path_csv)
        identificador = 1
        index_centroide = 0
        contador += 1
        listaObjetos.clear()
    
def calcular_precision_dice(nombre_imagenes, tipo):  #El nombre de las imagenes segmentadas manualmente y las segmentadas usando el modelo tienen el mismo nombre
    
    path_preds = '../Avance #3 Proyecto ACS/SegmentacionCelulas/preds/' if tipo == 0 else '../SegmentacionCelulas/preds/'
    path_seg_manual = '../Avance #3 Proyecto ACS/GT2/' if tipo == 0 else '../GT2/'
    path_csv = '../Avance #3 Proyecto ACS/CSV/' if tipo == 0 else '../CSV/'
    lista_porcentajes = []
    lista_promedio = []
    for nombre_img in nombre_imagenes:
        
        imagen_modelo = Image.open(path_preds + nombre_img)
        imagen_manual = Image.open(path_seg_manual + nombre_img)
        
        arr_img_modelo = np.asarray(imagen_modelo).copy()
        arr_img_modelo[arr_img_modelo>0] = 1
            
        arr_img_manual = np.asarray(imagen_manual).copy()
        arr_img_manual[arr_img_manual>0] = 1
        
        width,height = imagen_modelo.size
        
        denominador = np.matrix(arr_img_modelo).sum() + np.matrix(arr_img_manual).sum()
        numerador = 0
        
        for ancho in range(width):
            for altura in range(height):
                numerador += arr_img_modelo[ancho][altura] * arr_img_manual[ancho][altura]
        numerador*=2 
        
        coeficiente_dice = numerador/denominador
        lista_porcentajes.append(coeficiente_dice * 100)
        lista_promedio.append("-")
        
    nombre_imagenes.append("-")
    lista_promedio.append(str(np.mean(lista_porcentajes)))
    lista_porcentajes.append("-")
    
    diccionario = {'Nombre de la Imagen': nombre_imagenes, 'Porcentaje de Precision':lista_porcentajes, 'Promedio Precision':lista_promedio}
    datos = pandas.DataFrame(diccionario)
    datos.to_csv(path_csv + 'datos_dice.csv')
        
        