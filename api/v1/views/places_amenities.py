#!/usr/bin/python3
""" amenities api"""

from flask import jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def amenity_place(place_id=None):
    """ amenities api"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        apimethod = ApiMethod()
        if not place_id:
            abort(400)
        mylist = apimethod.get_object_byid("Place", place_id)
        if mylist:
            return make_response(jsonify(mylist), 200)
        else:
            abort(404)
    else:
        objects = storage.all('Place')
    if 'Place.' + place_id in objects.keys():
        myplace = objects['Place.' + place_id]
        amenity_list = getattr(myplace, 'amenity_ids')
        objs_list = []
        for amenity_id in amenity_list:
            objs_list.append(storage.get('Amenity', amenity_id).to_dict())
        return jsonify(objs_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST', 'DELETE'], strict_slashes=False)
def link_amenity(place_id=None, amenity_id=None):
    """ amenities api"""
    if request.method == 'POST':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            apimethod = ApiMethod()
            myplace = storage.get('Place', place_id)
            if not myplace:
                abort(404)
            myamenity = storage.get('Amenity', amenity_id)
            if not myamenity:
                abort(404)
            amenities_place = getattr(myplace, 'amenities')
            for amenity in amenities_place:
                if amenity.id == amenity_id:
                    mydict = amenity.to_dict()
                    return make_response(jsonify(mydict), 200)
            getattr(myplace, 'amenities').append(myamenity)
            storage.save()
            mydict = myamenity.to_dict()
            return make_response(jsonify(mydict), 201)
        else:
            objects = storage.all('Place')
            if 'Place.' + place_id in objects.keys():
                myplace = objects['Place.' + place_id]
            else:
                abort(404)
            myamenity = storage.get('Amenity', amenity_id)
            if not myamenity:
                abort(404)
            amenity_list = getattr(myplace, 'amenity_ids')
            if amenity_id in amenity_list:
                return jsonify(myamenity), 200
            getattr(myplace, 'amenity_ids').append(amenity_id)
            storage.save()
            storage.close()
            return jsonify(myamenity.to_dict()), 201

    if request.method == 'DELETE':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
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
        else:
            objects = storage.all('Place')
            if 'Place.' + place_id in objects.keys():
                myplace = objects['Place.' + place_id]
            else:
                abort(404)
            myamenity = storage.get('Amenity', amenity_id)
            if not myamenity:
                abort(404)
            amenity_list = getattr(myplace, 'amenity_ids')
            if amenity_id in amenity_list:
                getattr(myplace, 'amenity_ids').remove(amenity_id)
            else:
                abort(404)
            storage.save()
            storage.close()
            return jsonify({}), 200
