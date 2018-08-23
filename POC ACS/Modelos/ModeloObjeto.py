'''
Created on Aug 19, 2018

@author: Javier
'''

## \package Modelos
#  Contiene todo los atributos y comportamiento de la clase ObjetoImagen
#
#

 ## Descripcion de la clase Objeto Imagen.
 #
 #  Contiene la informacion y atributos (Centroide y Area) de los objetos encontrados en una imagen y un identificador para cada objeto.
 
class ObjetoImagen:
     ## El constructor
     # \param self
     # \param identificacion Es el identificador del objeto
     # \param centroide Caracteristica especial del objeto
     # \param area Caracteristica especial del objeto
    def __init__(self,identificacion,centroide,area):
        self.identificacion = identificacion
        self.centroide = centroide
        self.area = area
    