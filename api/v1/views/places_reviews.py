#!/usr/bin/python3
""" Review api"""

from flask import jsonify
from models import storage
from models.review import Review
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET', 'POST'], strict_slashes=False)
def review_place(place_id=None):
    """ place api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        mylist = apimethod.get_object_byid("Place", place_id, 'reviews')
        if mylist:
            return jsonify(mylist), 200
        else:
            abort(404)

    if request.method == 'POST':
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in request.json:
            return jsonify({'error': 'Missing user_id'}), 400
        if 'text' not in request.json:
            return jsonify({'error': 'Missing text'}), 400
        mydict = request.get_json()
        myuser = storage.get('User', mydict['user_id'])
        if not myuser:
            abort(404)
        myobj = storage.get('Place', place_id)
        if myobj:
            mydict['state_id'] = state_id
            newObjDict = apimethod.create_object(City, **mydict)
        else:
            abort(404)
        return jsonify(newObjDict), 201


@app_views.route("/reviews/<review_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review(review_id=None):
    """ review api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        mydict = apimethod.get_one_object("Review", review_id)
        if not mydict:
            abort(404)
        else:
            return make_response(jsonify(mydict), 200)
    if request.method == 'DELETE':
        deleteObj = apimethod.delete_one_object("Review", review_id)
        if not deleteObj:
            abort(404)
        else:
            return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)
        updObjDict = apimethod.update_objects("Review", review_id, **mydict)
        if updObjDict:

            return jsonify(updObjDict), 200
        else:
            abort(404)
