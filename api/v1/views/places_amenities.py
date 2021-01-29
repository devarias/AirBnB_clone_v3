#!/usr/bin/python3
"""Review module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models import storage
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == 'db':
    from models.place import place_amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_places_amenities(place_id):
    """get information for all amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids
    amenities = []
    for obj in place_amenity:
        amenities.append(obj.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity_by_id(place_id, amenity_id):
    """delete amenity by id"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids
    if amenity not in place_amenity:
        abort(404)
    place_amenity.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity_create(place_id, amenity_id):
    """create a new amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids
    if amenity in place_amenity:
        return jsonify(amenity.to_dict()), 200
    place_amenity.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
