"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

Sebastian = {
    "first_name": "Sebastian",
    "last_name": jackson_family.last_name,
    "age": 25,
    "lucky_numbers": [7, 27, 13]
}

Aitor = {
    "first_name": "Aitor",
    "last_name": jackson_family.last_name,
    "age": 30,
    "lucky_numbers": [11, 21, 31]
}

Albert = {
    "first_name": "Albert",
    "last_name": jackson_family.last_name,
    "age": 55,
    "lucky_numbers": [7, 35, 29]
}

jackson_family.add_member(Sebastian)
jackson_family.add_member(Aitor)
jackson_family.add_member(Albert)



@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['DELETE'])

def delete_member(id):
    funciona = jackson_family.delete_member(id)
    if funciona:
        return jsonify({"message": "Member deleted successfully"}), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    miembro = jackson_family.get_member(id)
    if miembro:
        return jsonify(miembro), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json

    jackson_family.add_member(data)
    return jsonify("miembro añadido"), 200



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
