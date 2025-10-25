from flask import Blueprint, jsonify, request, current_app
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    mongo = current_app.extensions['pymongo']
    users = list(mongo.db.users.find())
    for user in users:
        user['id'] = str(user['_id'])
        del user['_id']
    return jsonify(users)

@user_bp.route('/users', methods=['POST'])
def create_user():
    mongo = current_app.extensions['pymongo']
    data = request.json
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username and email are required'}), 400
    user = {
        'username': data['username'],
        'email': data['email']
    }
    result = mongo.db.users.insert_one(user)
    user['id'] = str(result.inserted_id)
    return jsonify(user), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    mongo = current_app.extensions['pymongo']
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['id'] = str(user['_id'])
    del user['_id']
    return jsonify(user)

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    mongo = current_app.extensions['pymongo']
    data = request.json
    update_data = {}
    if 'username' in data:
        update_data['username'] = data['username']
    if 'email' in data:
        update_data['email'] = data['email']
    result = mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    user['id'] = str(user['_id'])
    del user['_id']
    return jsonify(user)

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo = current_app.extensions['pymongo']
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return '', 204
