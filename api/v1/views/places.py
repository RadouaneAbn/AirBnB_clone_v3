#!/usr/bin/python3
"""
view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import Blueprint, abort, request
from werkzeug.exceptions import BadRequest
from models import storage
from models.city import City
from models.place import Place
from models.user import User


def get_object_by_id(cls, obj_id):
    """  """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_views.route(
        "/cities/<city_id>/places",
        methods=['GET'],
        strict_slashes=False)
def retrive_places_by_city(city_id):
    """  """
    city = get_object_by_id(City, city_id)
    if not city:
        abort(404)
    return [place.to_dict() for place in city.places]


@app_views.route(
        "/places/<place_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_place(place_id):
    """  """
    place = get_object_by_id(Place, place_id)
    if not place:
        abort(404)
    return place.to_dict()


@app_views.route(
        "/places/<place_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    place = get_object_by_id(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route(
        "/cities/<city_id>/places",
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    city = get_object_by_id(City, city_id)
    if city is None:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'user_id' not in request_data:
        abort(400, description="Missing user_id")

    user_id = request_data['user_id']
    user = get_object_by_id(User, user_id)
    if user is None:
        abort(404)

    if 'name' not in request_data:
        abort(400, description="Missing name")

    new_place = Place()
    new_place.name = request_data['name']
    new_place.user_id = user_id
    new_place.city_id = city_id
    new_place.save()
    return new_place.to_dict(), 201


@app_views.route(
        "/places/<place_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_place(place_id):
    place = get_object_by_id(Place, place_id)
    if not place:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'city_id', 'user_id'):
            setattr(place, key, value)

    place.save()
    return place.to_dict(), 200
