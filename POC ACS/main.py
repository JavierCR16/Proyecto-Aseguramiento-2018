from flask import Flask, render_template, request,session,redirect, url_for

from Gestores import gestorCSV, gestorImagenes, gestorKeras
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

## Descripcion de la funcion guardarImagen
#
#  Se encarga de recibir la imagen seleccionada por el usuario y la almacena en el directorio de salida especificado
#  \return Comando para visualizar la pagina de cargado y guardado de imagenes
def guardarImagen():
    nombreArchivo = request.files['file']
    __directorioArchivo = request.form.get("directorioArchivo")
    gestorImagenes.guardarImagen(nombreArchivo,__directorioArchivo)
    
    return render_template("imagen.html")

@app.route('/cargarModelo', methods = ['POST']) 
def cargarModelo():
    gestorKeras.cargarModelo(request.form.get("name"))
    
    return render_template("modeloKeras.html")

@app.route('/guardarModelo', methods = ['POST'])    
def guardarModelo():
    __model_name = request.form.get("model_name")
    __filter_number = request.form.get("filter_number")
    __shape_tuple = request.form.get("shape_tuple")
    __str_activation = request.form.get("str_activation")
    __optim = request.form.get("optim")
    __loss_function = request.form.get("loss_function")
    __num_epochs = request.form.get("num_epochs")
    __b_size = request.form.get("b_size")
    gestorKeras.guardarModelo(__model_name, __filter_number, __shape_tuple, __str_activation, __optim, __loss_function, __num_epochs, __b_size)
 
    return render_template("modeloKeras.html")

if __name__ == '__main__':

    app.run(debug=True)