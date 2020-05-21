"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, base64
from flask import Flask, request, jsonify, url_for, Response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from models import Users, Packages, db


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Buffers variables, to get data every 2 seconds from ScanStation
img = "";
Length = "";
Width = "";
Height = "";
Weight = "";

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user_query = Users.query.filter_by(email=email).first()
    
    if user_query is None:
        return jsonify({"msg": "User not exist, go signUP"}), 404
    else:
        if email != user_query.email or password != user_query.password:
            return jsonify({"msg": "Bad username or password"}), 401
        else:
            # Identity can be any data that is json serializable
            ret = {'jwt': create_jwt(identity=email), 'lvl': user_query.role_id}
            return jsonify(ret), 200

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    email = params.get('email', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    email_query = Users.query.filter_by(email=email).first()
    if email_query is not None:
        return jsonify({"msg": "Email already exist"}), 401
    
    name_query = Users.query.filter_by(username=username).first()
    if name_query is not None:
        return jsonify({"msg": "User name already exist"}), 401

    user = Users(username=username, email=email, password=password, role_id=1)
    db.session.add(user)
    db.session.commit()

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username), 'lvl': 3}
    return jsonify(ret), 200


# Protect a view with jwt_required, which requires a valid jwt
# to be present in the headers.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity()
    query_all = Packages.query.all()
    all_Packages = list(map(lambda x: x.serialize(), query_all))
    return jsonify(all_Packages), 200

@app.route('/userProtected', methods=['GET'])
@jwt_required
def userProtected():
    # Access the identity of the current user with get_jwt_identity()
    query_all = Users.query.all()
    all_Users = list(map(lambda x: x.serialize(), query_all))
    return jsonify(all_Users), 200

@app.route('/updateUserName', methods=['PUT'])
@jwt_required
def updateUserName():
    # Access the identity of the current user with get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    oldUsername = params.get('olduser', None)
    newUsername = params.get('newuser', None)
    if not oldUsername:
        return jsonify({"msg": "Missing olduser parameter"}), 400
    if not newUsername:
        return jsonify({"msg": "Missing newuser parameter"}), 400
    
    name_query = Users.query.filter_by(username=oldUsername).first()    
    name_query.username = newUsername
    db.session.commit()

    return jsonify({"msg": "User name updated"}), 200

@app.route('/deleteUser', methods=['DELETE'])
@jwt_required
def deleteUser():
    # Access the identity of the current user with get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    name = params.get('name', None)
    
    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    
    user1 = Users.query.get(name)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify({"msg": "User deleted"}), 200


@app.route('/api/test', methods=['POST'])
def test():
    global img, Length, Width, Height, Weight

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    img = params.get('img', None)
    Length = params.get('Length', None)
    Width = params.get('Width', None)
    Height = params.get('Height', None)
    Weight = params.get('Weight', None)

    fh = open("imageToSave.jpg", "wb")
    fh.write(base64.b64decode(img))
    fh.close()

    print(Length,Width,Height,Weight)
    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received'}

    return Response(response=response, status=200, mimetype="application/json")

@app.route('/api/test/get', methods=['GET'])
def test_get():

    response_body = {
        "img": img,
        "Length": Length,
        "Width": Width,
        "Height": Height,
        "Weight": Weight
    }

    return jsonify(response_body), 200

@app.route('/savePackage', methods=['POST'])
@jwt_required
def savePackage():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    img = params.get('img', None)
    Length = params.get('Length', None)
    Width = params.get('Width', None)
    Height = params.get('Height', None)
    Weight = params.get('Weight', None)

    if not img:
        return jsonify({"msg": "Missing img parameter"}), 400
    if not Length:
        return jsonify({"msg": "Missing Length parameter"}), 400
    if not Width:
        return jsonify({"msg": "Missing Width parameter"}), 400
    if not Height:
        return jsonify({"msg": "Missing Height parameter"}), 400
    if not Weight:
        return jsonify({"msg": "Missing Weight parameter"}), 400

    pack = Packages(tracking="z00n", length=Length, height=Width, width=Height, weight=Weight)
    db.session.add(pack)
    db.session.commit()

    return jsonify({"msg": "Package inserted"}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
