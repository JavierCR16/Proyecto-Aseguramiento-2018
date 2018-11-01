"""
docstring
"""

from flask import Flask, render_template, request
from Gestores.gestor_imagenes import GestorImagenes
from SegmentacionCelulas import unet_CellSegmentation as segmentador


APP = Flask(__name__)
APP.secret_key = "something-from-os.urandom(24)"


@APP.route('/')
def main():
    """"
    Docstring
    """
    gestor_imagenes = GestorImagenes()
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

    __directorio_imagenes = request.form.get("directorioArchivos")
    gestor_imagenes = GestorImagenes()
    imagenes_nombres = sorted(gestor_imagenes.obtener_imagenes(__directorio_imagenes))
    segmentador.predict()
    path_pred = '../Avance #2 Proyecto ACS/SegmentacionCelulas/preds'
    imagenes_pred = sorted(gestor_imagenes.obtener_nombre_preds(path_pred))
    gestor_imagenes.guardar_en_archivos()

    return render_template('cargadoDeImagenes.html',
                           nombresImagenes=imagenes_nombres, nombresPred=imagenes_pred)


if __name__ == '__main__':

    APP.run(debug=True)
    