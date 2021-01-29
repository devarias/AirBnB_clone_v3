#!/usr/bin/python3
"""
    It’s time to start your API!

    '/status' : 'Display: API Status with json file'
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """API Status with json file"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def counter():
    """A json file with the amount of objects in the classes"""
    return jsonify({"states": storage.count("State"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "users": storage.count("User"),
                    "reviews": storage.count("Review"),
                    "amenities": storage.count('Amenity')})
