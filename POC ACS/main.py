from flask import Flask, render_template, request,session,redirect, url_for

from Gestores import gestorCSV,gestorImagenes
from Modelos.ModeloObjeto import *


app = Flask(__name__)
app.secret_key = "something-from-os.urandom(24)"

## Descripcion de la funcion setVariablesDeSesion
#
#  Se encarga de definir cada una de las variables de sesion a utilizar.
#  \return Nada
def setVariablesDeSesion():
    session['listaObjetos'] = []
    
@app.route('/')

## Descripcion de la funcion main
#
#  Inicializa las variables de Sesion y redirige a la pagina web
#  \return Comando para visualizar la pagina de generacion del CSV
def main():
    setVariablesDeSesion()
    return render_template('csvPandas.html') 

@app.route('/cambioPantalla', methods = ['POST'])

## Descripcion de la funcion cambioPantalla
#
#  Se encarga de establecer la pantalla a mostrar de html dependiendo de la seleccion del usuario en la interfaz
#  \return Comando para visualizar la pagina de generacion de CSV, cargado y guardado de imagenes y cargado de modelos en Keras
def cambioPantalla():
    valorBoton = request.form.get("cambiar")
    
    if(valorBoton == "imagen"):
        return render_template("imagen.html")
    elif(valorBoton == "csv"):
        return render_template("csvPandas.html")
    elif(valorBoton == "keras"):
        return render_template("modeloKeras.html")

@app.route('/registrarPersonas', methods=['POST'])

## Descripcion de la funcion registrarPersonas
#
#  Se encarga de recibir los datos ingresados por el usuario y los almacena para ser usados en conjunto posteriormente
#  \return Comando para visualizar la pagina de generacion del CSV
def registrarPersonas():
    __numero = request.form.get("numero")
    __centroide = request.form.get("centroide")
    __area = request.form.get("area")
    
    objetos = session['listaObjetos']
    objetos.append(ObjetoImagen(__numero,__centroide,__area).__dict__)
    session['listaObjetos'] = objetos
                                                           
    
    return render_template("csvPandas.html")

@app.route('/generarCSV', methods = ['POST'])

## Descripcion de la funcion generarCSV
#
#  Se encarga de llamar a la funcion almacenada en el modulo de manejo de CSV
#  \return Comando para visualizar la pagina de generacion del CSV
def generarCSV():
    __directorioCSV = request.form.get("directorioCSV")
    gestorCSV.registroObjetos(session['listaObjetos'],__directorioCSV)

    return render_template("csvPandas.html")

@app.route('/guardarImagen', methods = ['POST'])

## Descripcion de la funcion generarCSV
#
#  Se encarga de recibir la imagen seleccionada por el usuario y la almacena en el directorio de salida especificado
#  \return Comando para visualizar la pagina de cargado y guardado de imagenes
def guardarImagen():
    nombreArchivo = request.files['file']
    __directorioArchivo = request.form.get("directorioArchivo")
    gestorImagenes.guardarImagen(nombreArchivo,__directorioArchivo)
    
    return render_template("imagen.html")

if __name__ == '__main__':

    app.run(debug=True)