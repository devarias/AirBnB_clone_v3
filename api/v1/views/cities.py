#!/usr/bin/python3
"""City module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """get information for all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """get information for the specified city"""
    obj = storage.get(City, city_id)
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """delete city by id"""
    obj = storage.get(City, city_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city_create(state_id):
    """create a new city"""
    conten = request.get_json()
    if conten is None:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if conten.get('name') is None:
        return "Missing name", 400
    else:
        city = City(**conten)
        city.state_id = state_id
        city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update a city"""
    if request.get_json() is None:
        return "Not a JSON", 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict()), 200
