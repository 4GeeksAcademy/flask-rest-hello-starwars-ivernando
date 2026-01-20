"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Usuario, PlanetaFavorito, PersonajeFavorito
from sqlalchemy import select 
from admin import PersonajeFavoritoAdmin, PlanetaFavoritoAdmin
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/personajes', methods=['GET'])
def get_personajes():

    personajes = db.session.execute(select(Personaje)).scalars().all()

    results_personajes = list(map(lambda personaje: personaje.serialize(), personajes))

    return jsonify(results_personajes), 200


@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):

    personaje = db.session.get(Personaje, personaje_id )

    if personaje is None:
       return jsonify({"message": "Personaje no encontrado"}), 404

    return jsonify(personaje.serialize()), 200


@app.route('/planetas', methods=['GET'])
def get_planetas():

    planetas = db.session.execute(select(Planeta)).scalars().all()

    results_planetas = list(map(lambda planeta: planeta.serialize(), planetas))

    return jsonify(results_planetas), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):

    planeta = db.session.get(Planeta, planeta_id )

    if planeta is None:
       return jsonify({"message": "Planeta no encontrado"}), 404

    return jsonify(planeta.serialize()), 200


@app.route('/usuarios', methods=['GET'])
def get_usuarios():

    usuarios = db.session.execute(select(Usuario)).scalars().all()

    results_usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))

    return jsonify(results_usuarios), 200

@app.route('/usuarios/favoritos', methods=['GET'])
def get_personajes_favoritos():

    usuario = db.session.get(Usuario, 1)

 
    return jsonify(usuario.serialize()), 200

@app.route('/planetas/favoritos', methods=['POST'])
def addfav_planeta():

    body = request.get_json()
    usuario_id = 1 
    planeta_id = body.get("planeta_id")

    planeta = db.session.get(Planeta, planeta_id)
    if planeta is None:
     return jsonify({"msg": "Planeta no existe"}), 404
   

    favorito = PlanetaFavorito(
        usuario_id= usuario_id,
        planeta_id= planeta_id
    )

    db.session.add(favorito)
    db.session.commit()
    

    return jsonify({"msg": "Planeta agregado a favoritos"}), 201
    

@app.route('/personajes/favoritos', methods=['POST'])
def addfav_personaje():

    body = request.get_json()
    usuario_id = 1 
    personaje_id = body.get("int:personaje_id")

    personajefav = db.session.get(Personaje, personaje_id)
    if personajefav is None:
     return jsonify({"msg": "personaje no existe"}), 404
   

    favorito = PersonajeFavorito(
        usuario_id= usuario_id,
        personaje_id= personaje_id
    )

    db.session.add(favorito)
    db.session.commit()
    

    return jsonify({"msg": "personaje agregado a favoritos"}), 201
    


@app.route('/personajes/favoritos/<personaje_id>', methods=['DELETE'])
def deletefav_personajes(personaje_id):

    
    usuario_id = 1

    personaje = db.session.execute(
        select(PersonajeFavorito)
        .where( PersonajeFavorito.personaje_id == personaje_id,
               PersonajeFavorito.usuario_id == usuario_id )).scalar_one_or_none()
   
    if personaje is None:
     return jsonify({"msg": "Personaje favorito no encontrado"}), 404

   
    db.session.delete(personaje)
    db.session.commit()

    
    usuario = db.session.get(Usuario, usuario_id)

    return jsonify(usuario.serialize()), 200



@app.route('/planetas/favoritos/<planeta_id>', methods=['DELETE'])
def deletefav_planetas(planeta_id):

    
    usuario_id = 1

    planeta = db.session.execute(
        select(PlanetaFavorito)
        .where( PlanetaFavorito.planeta_id == planeta_id,
               PlanetaFavorito.usuario_id == usuario_id )).scalar_one_or_none()
   
    if planeta is None:
     return jsonify({"msg": "Planeta favorito no encontrado"}), 404

   
    db.session.delete(planeta)
    db.session.commit()

    
    usuario = db.session.get(Usuario, usuario_id)

    return jsonify(usuario.serialize()), 200








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
