from pickle import TRUE
from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import pymongo
import requests
from bs4 import BeautifulSoup



MONGO_USER="AC1904"
MONGO_PASS="Tuity15"
MONGO_TIEMPO_FUERA=1000
mongo_uri="mongodb+srv://"+MONGO_USER+":"+MONGO_PASS+"@databasenosql.d6kk5u7.mongodb.net/?retryWrites=true&w=majority"

MONGO_BASEDATOS="OsaResort"
MONGO_COLECCION="Clientes"

MONGO_COLECCION2="Actividades"
MONGO_COLECCION3="TipoCambio"

cliente=MongoClient(mongo_uri,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
basedatos=cliente[MONGO_BASEDATOS]
coleccion=basedatos[MONGO_COLECCION]

coleccionActividades = basedatos[MONGO_COLECCION2]
coleccionTipoCambio = basedatos[MONGO_COLECCION3]

app = Flask(__name__)
app.secret_key = '123456789ABCD'


@app.route('/')
def ingreso():
    return render_template('ingreso.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/reservaciones')
def reservaciones():
    return render_template('reservaciones.html')

#----------------- CRUD Actividades -----------------

@app.route('/actividades')
def actividades():
    actividades = coleccionActividades.find()

    return render_template('actividades.html', actividades=actividades)


@app.route('/actividadesCrear')
def actividadesCrear():
    return render_template('actividadesCrear.html')


@app.route('/registrarActividad', methods=['POST'])
def registrarActividad():
    actividad = request.form['inputActividad']
    clima = request.form['inputClima']
    ultimoID = 0

    actividades = coleccionActividades.find({}, {"_id": 1})

    for dato in actividades:
        if (dato["_id"] > ultimoID):
            ultimoID = dato["_id"]
        

    idActividad = ultimoID + 1

    documento = {"_id": idActividad, "Actividad": actividad, "ClimaDePreferencia": clima}

    coleccionActividades.insert_one(documento)

    return redirect('/actividades')


@app.route('/actividadesEditar')
def actividadesEditar():
    idActividad = int (request.args.get('id'))
    actividad = coleccionActividades.find_one({"_id": idActividad})

    print(actividad['ClimaDePreferencia'])

    return render_template('actividadesEditar.html', actividad=actividad)


@app.route('/modificarActividad', methods=['POST'])
def modificarActividad():
    idActividad = int (request.args.get('id'))
    #actividad = coleccionActividades.find_one({"_id": idActividad})
    actividadNueva = request.form['inputActividad']
    climaNuevo = request.form['inputClima']
    idBuscado = {"_id": idActividad}

    # print("Id editado: " + str (actividad['_id'])
    #                             + "\nNueva actividad: " + actividadNueva
    #                             + "\nNuevo clima: " + climaNuevo)
    
    nuevosValores = {"$set": {"Actividad": actividadNueva, "ClimaDePreferencia": climaNuevo}}

    coleccionActividades.update_one(idBuscado, nuevosValores)

    return redirect('/actividades')


@app.route('/eliminarActividad', methods=['GET', 'POST'])
def eliminarActividad():
    idActividad = int (request.args.get('id'))
    coleccionActividades.delete_one({'_id': idActividad})

    flash('La actividad ha sido eliminada.')

    return redirect('/actividades')

#------------------------------------------------------------------------


@app.route('/clientes')
def clientes():
        clientes = coleccion.find()
        return render_template('clientes.html', clientes=clientes)


@app.route('/identificacion', methods=['POST'])
def identificacion():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    results = coleccion.find({'correo': correo, 'contrasena': contrasena})
    try:
        for resultado in results:
            if resultado['nombre'] is None:
                print('User not exists.')
                return render_template('ingreso.html')
            else:
                print(results)
                return render_template('principal.html')
    except pymongo.errors.ConectionFailure as error:
            print(error) 

if __name__ == '__main__':
    app.run(debug=TRUE)