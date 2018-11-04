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


## Descripcion de la funcion registroObjetos
#
#  Se encarga de agrupar los datos, que provienen en diccionarios, en tres categorias las cuales seran cargadas en un archivo CSV
#  \param listaObjetos Es una lista de diccionarios y cada diccionario contiene los atributos de area, centroide e identificacion
#  \param directorio Es el directorio de salida en donde se va a generar el CSV
#  \return Nada
def registroObjetos(listaObjetos,contador): #ObjetoImagen(__numero,__centroide,__area).__dict__
    try:
        listaIdentificacion= [d["identificacion"] for d in listaObjetos ]
        listaCentroide= [d["centroide"] for d in listaObjetos]
        listaArea = [d["area"] for d in listaObjetos]
        diccionario = {'Identificacion':listaIdentificacion,'Centroide': listaCentroide,'Area': listaArea}
        
        datos = pandas.DataFrame(diccionario)
        datos.to_csv('../Avance #3 Proyecto ACS/CSV/objetos_celulas' +str(contador)+'.csv')
        return True
    except:
        return False
    
def procesar_informacion_celulas(lista_archivos_celulas, lista_centroides,identificadores_archivos):
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
        
        registroObjetos(listaObjetos, identificadores_archivos[contador].split('.')[0])
        identificador = 1
        index_centroide = 0
        contador += 1
        listaObjetos.clear()
    