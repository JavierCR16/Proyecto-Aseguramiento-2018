'''
Created on Nov 2, 2018

@author: Javier
'''
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
from operator import itemgetter
import operator
from PIL import ImageDraw

def revisar_pixeles_aliados(arregloImagen, ancho, altura, coordenadas):

    if(not esNegro(arregloImagen,ancho,altura) and (ancho,altura) not in coordenadas):

        coordenadas.append((ancho,altura))

        revisar_pixeles_aliados(arregloImagen, ancho+1, altura, coordenadas) #derecha
        revisar_pixeles_aliados(arregloImagen, ancho-1, altura, coordenadas) #izquierda
        revisar_pixeles_aliados(arregloImagen, ancho, altura+1, coordenadas) #abajo
        revisar_pixeles_aliados(arregloImagen, ancho, altura-1, coordenadas) #arriba

        return coordenadas

    return coordenadas
        
def esNegro(arregloImagen, ancho, altura):

    if(arregloImagen[ancho][altura]==0):#[0] == 0 and  arregloImagen[ancho][altura][1] == 0 and arregloImagen[ancho][altura][2] == 0):
        return True
    return False

def pixelVerificado(ancho,altura,lista_celulas):
    if(lista_celulas==[]):
        return False
    #print(lista_celulas)
    for lista_coordenadas in lista_celulas:
        if((ancho,altura) in lista_coordenadas):
            return True
    return False

def obtener_coordenadas_celulas(path_file):

    lista_celulas = []
    
    imagen = Image.open(path_file)
    arr_imagen= np.asarray(imagen)
    width, height = imagen.size
    for ancho in range(width):
        for altura in range(height):
            if (not pixelVerificado(ancho,altura,lista_celulas)):
                nuevas_coordenadas = revisar_pixeles_aliados(arr_imagen,ancho,altura,[])

                if(nuevas_coordenadas != []):
                    lista_celulas.append(nuevas_coordenadas)
                    #return lista_celulas
    return lista_celulas

def obtener_minimos_maximos(lista_coordenadas_celula):
    lista_minimos_maximos = []
    
    for coordenadas_celula in lista_coordenadas_celula:
        punto_maximo_y = min(coordenadas_celula,key=itemgetter(0))[::-1]
        punto_minimo_y = max(coordenadas_celula,key=itemgetter(0))[::-1]
        punto_maximo_x = max(coordenadas_celula,key=itemgetter(1))[::-1]
        punto_minimo_x = min(coordenadas_celula,key=itemgetter(1))[::-1]

        listay = [punto_minimo_y, punto_maximo_y]
        listax = [punto_minimo_x, punto_maximo_x]
        
        lista_minimos_maximos.append((listax.copy(),listay.copy()))

    return lista_minimos_maximos

def generar_rango_tuplas(fijo, rango, eje):

    lista_rangos = []

    valores = list(range(rango[0],rango[1]))
    
    while(valores != []):
        if eje == 'x':
            lista_rangos.append([fijo,valores[0]])
        else:
            lista_rangos.append([valores[0],fijo])
                
        valores = valores[1:]
    return lista_rangos

def getCellCenter(immat, X, Y):

    m = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            m[x,y] = immat[(x,y)] != 0
             
    m = m / np.sum(np.sum(m))

    dx = np.sum(m,1)
    dy = np.sum(m,0)

    cx = np.sum(dx * np.arange(X))
    cy = np.sum(dy * np.arange(Y))
    
    return(int(round(cx)), int(round(cy)))

def generar_centroides_celulas(lista_tupla_ejes, path_imagen):
    lista_centros = []
    for tupla_ejes in lista_tupla_ejes:
        imagen_a_recortar = Image.open(path_imagen)
    
        minx = list(tupla_ejes[0][0])
        maxx = list(tupla_ejes[0][1])
        miny = list(tupla_ejes[1][0])
        maxy = list(tupla_ejes[1][1])
    
        minx[0]-=1
        maxx[0]+=1
        miny[1]+=1
        maxy[1]-=1
    
        coordenadas_rectangulo = []
    
        pto_inicial = minx.copy()
        pto_inicial[1] = maxy[1] #Vertice Superior Izquierdo
    
        pto_inicial2 = minx.copy()
        pto_inicial2[1] = miny[1] #Vertice Inferior Izquierdo
    
        pto_inicial3 = maxx.copy()
        pto_inicial3[1] = maxy[1] #Vertice Superior Derecho
    
        pto_inicial4 = maxx.copy()
        pto_inicial4[1] = miny[1] #Vertice Inferior Derecho
    
    
        imagen_a_recortar = imagen_a_recortar.crop((pto_inicial[0],pto_inicial[1],pto_inicial4[0],pto_inicial4[1]))
    
        width, height = imagen_a_recortar.size
    
        arreglo_imagen_celula = np.asarray(imagen_a_recortar)
    
        centro = getCellCenter(arreglo_imagen_celula,height,width)
        
        centro = centro[::-1]
        
        centro_actualizado = tuple(map(operator.add, centro, pto_inicial))
        
        lista_centros.append(centro_actualizado)

    return lista_centros
    
def pintar_coordenadas(lista,path_file,path_coloreadas,path_static ,contador,coordenadas_centroides):
    imagen_color_etiq = Image.open(path_file)
    imagen_color_etiq = imagen_color_etiq.convert('RGB')

    etiquetar = ImageDraw.Draw(imagen_color_etiq)
    xy_etiquetado_desplazamiento = (-4,-4)
    
    font_definido = ImageFont.truetype("BRITANIC", 11)
    index = 1
    for listaCoordenadas in lista:
        for i in range(len(listaCoordenadas)):
            imagen_color_etiq.putpixel(listaCoordenadas[i][::-1],(255,255,255))
    
    
    for centroide in coordenadas_centroides: #HAY QUE QUITARLO
        centroide_tmp = list(centroide).copy()
        centroide_tmp = tuple(map(operator.add, centroide_tmp, xy_etiquetado_desplazamiento))
        etiquetar.text(centroide_tmp,str(index),fill = (255,0,0), font=font_definido)
        index +=1
    imagen_color_etiq.save(path_static + 'predColorEtiq' +str(contador)+'.png')
    imagen_color_etiq.save(path_coloreadas + 'predColorEtiq' +str(contador)+'.png')
    
    
