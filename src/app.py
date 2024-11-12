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
last_name = "Jackson"

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members/', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body =  members

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({'msg': 'Not found'}), 404
        # Ensure the response contains the required keys
        response_body = {
            'name': member['first_name'],
            'id': member['id'],
            'age': member['age'],
            'lucky_numbers': member['lucky_numbers']
        }
        return jsonify(response_body), 200
    except Exception:
        return jsonify({'msg': 'Internal Server Error'}), 500

@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json
    members = jackson_family.add_member(new_member) # this is the method for adding a new family member to the list. 
    response_body = {members}
    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def post_member():
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
                'age': body['age'],
                'lucky_numbers': body['lucky_numbers']
             }
    members = jackson_family.add_member(new_member)
    return jsonify({'msg': 'OK', 'members': members })

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
