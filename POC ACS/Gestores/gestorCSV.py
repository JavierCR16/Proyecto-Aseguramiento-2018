'''
Created on Aug 19, 2018

@author: Javier
'''

## \package Gestores
#  Contiene todas las funciones asociadas al manejo de archivos de extension CSV utilizando la libreria PANDAS
#

import pandas
from collections import namedtuple


## Descripcion de la funcion registroObjetos
#
#  Se encarga de agrupar los datos, que provienen en diccionarios, en tres categorias las cuales seran cargadas en un archivo CSV
#  \param listaObjetos Es una lista de diccionarios y cada diccionario contiene los atributos de area, centroide e identificacion
#  \return Nada
def registroObjetos(listaObjetos, directorio):
    try:
        listaIdentificacion= [d["identificacion"] for d in listaObjetos ]
        listaCentroide= [d["centroide"] for d in listaObjetos]
        listaArea = [d["area"] for d in listaObjetos]
        diccionario = {'Identificacion':listaIdentificacion,'Centroide': listaCentroide,'Area': listaArea}
        
        datos = pandas.DataFrame(diccionario)
        datos.to_csv(directorio)
        return True
    except:
        return False