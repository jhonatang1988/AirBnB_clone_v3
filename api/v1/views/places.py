#!/usr/bin/python3
""" places api"""

from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/cities/<city_id>/places",
                 methods=['GET', 'POST'], strict_slashes=False)
def place_city(city_id=None):
    """ places api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        mylist = apimethod.get_object_byid("City", city_id, 'places')
        return make_response(jsonify(mylist), 200)

    if request.method == 'POST':
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in request.json:
            return jsonify({'error': 'Missing user_id'}), 400

        if 'name' not in request.json:
            return jsonify({'error': 'Missing name'}), 400

        mydict = request.get_json()

        myuser = storage.get('User', mydict['user_id'])
        if not myuser:
            abort(404)

        myobj = storage.get('City', city_id)
        if myobj:
            mydict['city_id'] = city_id
            newObjDict = apimethod.create_object(Place, **mydict)
        else:
            abort(404)
        return make_response(jsonify(newObjDict), 201)


@app_views.route("/places/<place_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id=None):
    """ places api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if not place_id:
            abort(400)
        mydict = apimethod.get_one_object("Place", place_id)
        if not mydict:
            abort(404)
        else:
            return make_response(jsonify(mydict), 200)
    if request.method == 'DELETE':
        if place_id:
            deleteObj = apimethod.delete_one_object("Place", place_id)
            if not deleteObj:
                abort(404)
            else:
                return make_response(jsonify({}, 200))
        else:
            abort(400)

    if request.method == 'PUT':
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)
        updObjDict = apimethod.update_objects("Place", place_id, **mydict)
        if updObjDict:

            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)
