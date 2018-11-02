"""
docstring
"""

from flask import Flask, render_template, request
from Gestores.gestor_imagenes import GestorImagenes
from SegmentacionCelulas import unet_CellSegmentation as segmentador


APP = Flask(__name__)
APP.secret_key = "something-from-os.urandom(24)"
gestor_imagenes = GestorImagenes()

@APP.route('/')
def main():
    """"
    Docstring
    """
    gestor_imagenes.eliminar_directorios()
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
    gestor_imagenes.eliminar_directorios()
    __directorio_imagenes = request.form.get("directorioArchivos")
    imagenes_nombres = sorted(gestor_imagenes.obtener_imagenes(__directorio_imagenes))
    tiempos_imagenes,tiempo_total = segmentador.predict()  #VER DONDE PONER ESTO
    path_pred = '../Avance #3 Proyecto ACS/SegmentacionCelulas/preds'
    imagenes_pred = sorted(gestor_imagenes.obtener_nombre_preds(path_pred))
    cantidad_celulas = gestor_imagenes.colorear_etiquetar_imagenes()
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes=imagenes_nombres, nombresPred=imagenes_pred,
                           totalEjecucion = str(tiempo_total), cantidadCelulas = cantidad_celulas)

@APP.route('/guardarResultados', methods=['POST'])
def guardar_resultados():
    gestor_imagenes.guardar_en_archivos()
    return render_template('cargadoDeImagenes.html',
                           nombresImagenes = gestor_imagenes.lista_nombres, nombresPred= gestor_imagenes.lista_preds, 
                           cantidadCelulas = gestor_imagenes.cant_celulas_preds,
                           mensajeExito = 'Resultados guardados exitosamente!')

if __name__ == '__main__':

    APP.run(debug=True)
    