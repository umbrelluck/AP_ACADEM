from flask import make_response, jsonify
from flask_restful import Resource


class Lab1Get(Resource):
    def get(self):
        return make_response(jsonify({"message": "Hello World 000"}), 200)
