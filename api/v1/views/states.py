#!/usr/bin/python3
"""State module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get information for all states"""
    states = []
    for obj in storage.all("State").values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """get information for the specified state"""
    obj = storage.get(State, state_id)
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """delete state by id"""
    obj = storage.get(State, state_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state_create():
    """create a new state"""
    conten = request.get_json()
    if conten is None:
        return "Not a JSON", 400
    if conten.get('name') is None:
        return "Missing name", 400
    else:
        new_obj = State(**conten)
        storage.new(new_obj)
        storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    if request.get_json() is None:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    storage.save()
    return jsonify(state.to_dict()), 200
