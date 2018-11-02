'''
Created on Nov 2, 2018

@author: Javier
'''
from PIL import Image
import numpy as np

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

    if(arregloImagen[ancho][altura][0] == 0 and  arregloImagen[ancho][altura][1] == 0 and arregloImagen[ancho][altura][2] == 0):
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

def pintar_coordenadas(lista,path_file,path_coloreadas ,contador):
    imagen_color_etiq = Image.open(path_file)

    for listaCoordenadas in lista:
        for i in range(len(listaCoordenadas)):
            imagen_color_etiq.putpixel(listaCoordenadas[i][::-1],(255,255,255))
    imagen_color_etiq.save(path_coloreadas + 'predColorEtiq' +str(contador)+'.png')
    
