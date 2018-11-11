'''
Created on Nov 11, 2018

@author: Javier
'''

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import random as ran
from operator import itemgetter
import operator
from PIL import ImageDraw

def etiquetar_imagen(imagen_color_etiq, coordenadas_centroide, path_static, path_coloreadas,contador):
    
    etiquetar = ImageDraw.Draw(imagen_color_etiq)
    xy_etiquetado_desplazamiento = (-4,-4)
    
    font_definido = ImageFont.truetype("BRITANIC", 11)
    index = 1
    
    for centroide in coordenadas_centroide: #HAY QUE QUITARLO
        centroide_tmp = list(centroide).copy()
        centroide_tmp = tuple(map(operator.add, centroide_tmp, xy_etiquetado_desplazamiento))
        etiquetar.text(centroide_tmp,str(index),fill = (255,255,255), font=font_definido)
        index +=1
    imagen_color_etiq.save(path_static + 'predColorEtiq' +str(contador)+'.png')
    imagen_color_etiq.save(path_coloreadas + 'predColorEtiq' +str(contador)+'.png')