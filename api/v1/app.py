#!/usr/bin/python3
"""script that starts a Flask web application:
The application listens on 0.0.0.0, port 5000.
"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def use_teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Not found page 404"""
    return make_response(jsonify({'error': 'Not found'})), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
