# decorator for verifying the JWT
from functools import wraps

from flask import app, jsonify, request
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Unauthorized'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            data = jwt.decode(token, "AsCtVTHM73iTeaez8xMNt3Ruk3GhqdNS", algorithms=["HS256"])
        except:
            return jsonify({
                'message' : 'Invalid Authorization token.'
            }), 401
        # returns the current logged in users context to the routes
        # return  f(data, *args, **kwargs)
        return f(*args, **kwargs)
  
    return decorated