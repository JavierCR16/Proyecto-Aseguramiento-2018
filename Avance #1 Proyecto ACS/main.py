from flask import Flask, render_template, request,session,redirect, url_for
from Gestores import GestorImagenes
app = Flask(__name__)
app.secret_key = "something-from-os.urandom(24)"


@app.route('/')
def main():
    
    return render_template('cargadoDeImagenes.html') 

@app.route('/cargarImagenes', methods = ['POST'])
def cargarImagenes():
    
    __directorioImagenes = request.form.get("directorioArchivos")
    listaImagenes,listaNombres= GestorImagenes.obtenerImagenes(__directorioImagenes) #listaImagenes se envia al servidor,  listaNombres es para mostrar en el cliente
    
    return render_template('cargadoDeImagenes.html',nombresImagenes = listaNombres) 

if __name__ == '__main__':

    app.run(debug=True)
