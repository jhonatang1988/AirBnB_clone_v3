#!/usr/bin/python3
""" amenities api"""

from flask import jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def amenity_place(place_id=None):
    """ amenities api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        print("entre al GET")
        if not place_id:
            abort(400)
        mylist = apimethod.get_object_byid("Place", place_id)
        if mylist:
            return make_response(jsonify(mylist), 200)
        else:
            abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST', 'DELETE'], strict_slashes=False)
def link_amenity(place_id=None, amenity_id=None):
    """ amenities api"""
    apimethod = ApiMethod()
    if request.method == 'POST':
        myplace = storage.get('Place', place_id)
        if not myplace:
            abort(404)
        myamenity = storage.get('Amenity', amenity_id)
        if not myamenity:
            abort(404)
        amenities_place = getattr(myplace, 'amenities')
        print(amenities_place)
        for amenity in amenities_place:
            if amenity.id == amenity_id:
                mydict = amenity.to_dict()
                return make_response(jsonify(mydict), 200)
        getattr(myplace, 'amenities').append(myamenity)
        storage.save()
        mydict = myamenity.to_dict()
        return make_response(jsonify(mydict), 201)

    if request.method == 'DELETE':
        myplace = storage.get('Place', place_id)
        if not myplace:
            abort(404)
        myamenity = storage.get('Amenity', amenity_id)
        if not myamenity:
            abort(404)
        amenities_place = getattr(myplace, 'amenities')
        for amenity in amenities_place:
            if amenity.id == amenity_id:
                amenities_place.pop(amenity)
                return make_response(jsonify({}), 200)
        abort(404)
