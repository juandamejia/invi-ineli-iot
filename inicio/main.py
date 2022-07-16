from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.collation import Collation
import datetime,pytz
import json

basedatos = MongoClient(
    "mongodb+srv://juandamejia26:1036253366hola@cluster0.hn29h.mongodb.net/?retryWrites=true&w=majority"
)

print(basedatos.list_database_names())

app = Flask(__name__)
CORS(app)
oneArray = [0]
temperaturaVida = [0]

humedadArray = [0]
humedadVida = [0]

temperaturaArray = [0]
tempVida = [0]

luzArray = [0]
luzVida = [0]

e = [0]

collection = basedatos.invernadero.raspberry


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "GET":
        return render_template("index.html")
    else:

        a = request.form.get("tierra")
        b = request.form.get("humedad")
        c = request.form.get("temperatura")
        d = request.form.get("iluminacion")
        e = datetime.datetime.now(pytz.timezone('America/Bogota'))
        # oneArray.append(one)
        # humedadArray.append(humedad)
        # temperaturaArray.append(temperatura)
        #luzArray.append(luz)
        
        collection.insert_one({
          "fecha": e,
          "temperatura": c,
          "one": a,
          "humedad": b,
          "luz": d
        })
       # for registro in collection.find():
        # print(registro)
        return redirect("/")


@app.route("/api/one", methods=["GET", "POST"])
def api_one():
    get_database_mongo_data = collection.find_one()
    objet_filter = {
        "fecha": get_database_mongo_data["fecha"],
        "temperatura": get_database_mongo_data["humedad"],
        "luz": get_database_mongo_data["luz"],
        "humedad": get_database_mongo_data["temperatura"],
        "one": get_database_mongo_data["one"],
    }
    print(objet_filter)
    return objet_filter


@app.route("/api/all", methods=["GET", "POST"])
def api_fetchAll():
    get_database_mongo_data = [-1]
    for registro in collection.find():
        objet_filter = {
            "temperatura": registro["humedad"],
            "luz": registro["luz"],
            "humedad": registro["temperatura"],
            "one": registro["one"],
           "fecha": registro["fecha"]
        }
        get_database_mongo_data.append(objet_filter)
    return {"data": get_database_mongo_data}

app.run(host='0.0.0.0', port=81)