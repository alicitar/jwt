import pdb
from functools import wraps

import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response


app = Flask(__name__)

app.config["SECRET_KEY"] = "abc123"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'token is missing'}), 403

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
        except:
            return jsonify({'message' : 'token is invalid'}), 403

        return f(*args, **kwargs)
    return decorated


@app.route('/alive', methods=['GET'])
def live():
    return "its alive!!"

# @app.route('/login', methods=['GET'])
# def login():
#     auth = request.authorization
#     if auth and auth.password == 'asd':
#         token = jwt.encode({'user': auth.username, 'exp' : datetime.utcnow() + timedelta(minutes=5)}, app.config["SECRET_KEY"])

#         return jsonify({'token':token})

#     return make_response('Culd verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# SIN HEADER
# @app.route('/get-token/<id>', methods=['GET'])
# def get_token(id):
#     if id == 'asd':
#         token = jwt.encode({'exp' : datetime.utcnow() + timedelta(minutes=5)}, app.config["SECRET_KEY"])

#         return jsonify({'token':token})

#     return make_response('id is invalid', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# CON HEADER
@app.route('/get-token/', methods=['GET'])
def get_token():
    key = request.headers.get('wsEjemplo')
    if key == 'ZTMR@73pq':
        token = jwt.encode({'exp' : datetime.utcnow() + timedelta(minutes=5)}, app.config["SECRET_KEY"])

        return jsonify({'token':token})

    return make_response('Invalid key or value', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'token ok'})

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'this is for everyone'})



if __name__ == '__main__':
    app.run(debug=True, port=5001)



