'''
Created on Aug 19, 2018

@author: Javier
'''
import pandas
from collections import namedtuple

def registroObjetos(listaObjetos):
    listaIdentificacion= [d["identificacion"] for d in listaObjetos ]
    listaCentroide= [d["centroide"] for d in listaObjetos]
    listaArea = [d["area"] for d in listaObjetos]
    diccionario = {'Numero':listaIdentificacion,'Centroide': listaCentroide,'Area': listaArea}
    
    datos = pandas.DataFrame(diccionario)
    datos.to_csv('CSV/listaObjetos.csv')