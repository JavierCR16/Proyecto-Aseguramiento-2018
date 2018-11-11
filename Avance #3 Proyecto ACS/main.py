"""
docstring
"""

from flask import Flask, render_template, request
from Gestores.gestor_imagenes import GestorImagenes
from SegmentacionCelulas import unet_CellSegmentation as segmentador
from Gestores import gestor_csv
import os


APP = Flask(__name__)
APP.secret_key = "something-from-os.urandom(24)"
gestor_imagenes = GestorImagenes()

@APP.route('/')
def main():
    """"
    Docstring
    """
    gestor_imagenes.eliminar_directorios(0)
        
    return render_template('cargadoDeImagenes.html')


@APP.route('/cambioPantalla', methods=['POST'])
def cambio_pantalla():
    """"
    Docstring
    """

    valor_boton = request.form.get("cambiar")

    if valor_boton == "imagenes":
        return render_template('cargadoDeImagenes.html')
    return 0


# imagenes procesar,  nombres es para mostrar en el cliente
@APP.route('/cargarImagenes', methods=['POST'])
def cargar_imagenes():
    """"
    Docstring
    """
    gestor_imagenes.eliminar_directorios(0)
    path_pred = '../Avance #3 Proyecto ACS/SegmentacionCelulas/preds'
    path_etiq = '../Avance #3 Proyecto ACS/SegmentacionCelulas/predsColoreadasEtiquetadas'
    __directorio_imagenes = request.form.get("directorioArchivos")
    imagenes_nombres = gestor_imagenes.obtener_imagenes(__directorio_imagenes)
    
    lista_tiempos = tiempos_imagenes,tiempo_total = segmentador.predict()  #VER DONDE PONER ESTO DE TIEMPO IMAGENES
    
    imagenes_pred = gestor_imagenes.obtener_nombre_preds(path_pred)
    
    gestor_imagenes.colorear_etiquetar_imagenes(lista_tiempos)
    
    imagenes_etiq = gestor_imagenes.obtener_nombre_etiq(path_etiq)
    
    gestor_imagenes.tiempos_lista= lista_tiempos
    gestor_imagenes.formatear_tiempos()
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes=imagenes_nombres, nombresPred=imagenes_pred, nombresEtiq = imagenes_etiq,
                           totalEjecucion = gestor_imagenes.tiempos_lista[1], totalImagenes = gestor_imagenes.tiempos_lista[0],
                           cantidadCelulas = gestor_imagenes.cant_celulas_preds)

@APP.route('/guardarResultados', methods=['POST'])
def guardar_resultados():
    gestor_imagenes.guardar_en_archivos()
    
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes = gestor_imagenes.lista_nombres, nombresPred= gestor_imagenes.lista_preds
                           , nombresEtiq = gestor_imagenes.lista_etiq, cantidadCelulas = gestor_imagenes.cant_celulas_preds,
                           mensajeExito = 'Resultados guardados exitosamente!',totalEjecucion = gestor_imagenes.tiempos_lista[1],
                           totalImagenes = gestor_imagenes.tiempos_lista[0])

@APP.route('/guardarCSV', methods=['POST'])
def guardar_resultados_csv(): 
    gestor_csv.procesar_informacion_celulas(gestor_imagenes.coordenadas_celulas,gestor_imagenes.centroides,gestor_imagenes.lista_nombres,0)
    
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes = gestor_imagenes.lista_nombres, nombresPred= gestor_imagenes.lista_preds, 
                           nombresEtiq = gestor_imagenes.lista_etiq, cantidadCelulas = gestor_imagenes.cant_celulas_preds,
                           mensajeExito = 'Resultados guardados exitosamente!',totalEjecucion = gestor_imagenes.tiempos_lista[1],
                           totalImagenes = gestor_imagenes.tiempos_lista[0])

@APP.route('/guardarDICE', methods=['POST'])
def guardar_dice_csv():
    gestor_csv.calcular_precision_dice(gestor_imagenes.lista_preds,0)
    
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes = gestor_imagenes.lista_nombres, nombresPred= gestor_imagenes.lista_preds, 
                           nombresEtiq = gestor_imagenes.lista_etiq, cantidadCelulas = gestor_imagenes.cant_celulas_preds,
                           mensajeExito = 'Metrica de DICE aplicada exitosamente!',totalEjecucion = gestor_imagenes.tiempos_lista[1],
                           totalImagenes = gestor_imagenes.tiempos_lista[0])

if __name__ == '__main__':

    APP.run(threaded = False,debug=True)
    