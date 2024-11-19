"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({'msg': 'Not found'}), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400
    if 'first_name' not in body:
        return jsonify({'msg': 'El campo first_name es obligatorio'}), 400
    if 'age' not in body:
        return jsonify({'msg': 'El campo age es obligatorio'}), 400
    if 'lucky_numbers' not in body:
        return jsonify({'msg': 'El campo lucky_numbers es obligatorio'}), 400
    new_member = {
                'id': jackson_family._generateId(),
                'first_name': body['first_name'],
                'last_name': jackson_family.last_name,
                'age': body['age'],
                'lucky_numbers': body['lucky_numbers']
             }
    members = jackson_family.add_member(new_member)
    return jsonify({'msg': 'OK', 'members': members }), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result:
        return jsonify({'done': True}), 200
    return jsonify({'msg': 'Member not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)