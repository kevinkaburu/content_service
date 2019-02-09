import threading
from flask_mail import Mail, Message
from flask import current_app, request, jsonify, g
from functools import wraps
import tokenise


def resource_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page      
        if not request.headers["authorization"]:
            return {"status":"fail","message":"Login required"},401
        jwt_token = request.headers["authorization"]
        raw_data = tokenise.decrypt_token(jwt_token,current_app.config['JWT_KEY'])
        if raw_data is None:
             return {"status":"fail","message":"Login required"},401
        g.user = raw_data
        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)
   
    return wrap



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page      
        if not request.headers["authorization"]:
            return jsonify({"status":"fail","message":"Login required"}),401
        jwt_token = request.headers["authorization"]
        raw_data = tokenise.decrypt_token(jwt_token,current_app.config['JWT_KEY'])
        if raw_data is None:
             return {"status":"fail","message":"Login required"},401
        g.user = raw_data
        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)
   
    return wrap

