

from flask import Flask, render_template, request,session,redirect, url_for

from Gestores import gestorCSV,gestorImagenes
from Modelos.ModeloObjeto import *

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "something-from-os.urandom(24)"

   

def setVariablesDeSesion():
   

    session['listaObjetos'] = []
    
@app.route('/')
def main():
    setVariablesDeSesion()
    return render_template('csvPandas.html') 

@app.route('/cambioPantalla', methods = ['POST'])
def cambioPantalla():
    valorBoton = request.form.get("cambiar")
    
    if(valorBoton == "imagen"):
        return render_template("imagen.html")
    elif(valorBoton == "csv"):
        return render_template("csvPandas.html")
    elif(valorBoton == "keras"):
        return render_template("modeloKeras.html")

@app.route('/registrarPersonas', methods=['POST'])
def registrarPersonas():
    __numero = request.form.get("numero")
    __centroide = request.form.get("centroide")
    __area = request.form.get("area")
    
    objetos = session['listaObjetos']
    objetos.append(ObjetoImagen(__numero,__centroide,__area).__dict__)
    session['listaObjetos'] = objetos
                                                           
    
    return render_template("csvPandas.html")

@app.route('/generarCSV', methods = ['POST'])
def generarCsv():
    
    gestorCSV.registroObjetos(session['listaObjetos'])

    return render_template("csvPandas.html")

@app.route('/guardarImagen', methods = ['POST'])
def guardarImagen():
    nombreArchivo = request.files['file']
    __directorioArchivo = request.form.get("directorioArchivo")
    gestorImagenes.guardarImagen(nombreArchivo,__directorioArchivo)
    
    return render_template("imagen.html")

if __name__ == '__main__':

    app.run(debug=True)