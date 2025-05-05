from flask import Flask, request, jsonify
import database as database
import helpers as helpers 

app = Flask(__name__)

connection = database.connect_to_database()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing username and password'}), 400
    if 'username' not in data:
        return jsonify({'error': 'Missing username'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400

    username = data['username']
    password = data['password']

    if not helpers.is_valid_username(username):
        return jsonify({'error': 'Invalid username (must be 3-20 characters)'}), 400
    if not helpers.is_strong_password(password):
        return jsonify({'error': 'Invalid password (must be >=8 chars, with upper, lower, digit)'}), 400

    hashed_password = helpers.hash_password(password)

    if database.create_user(connection, username, hashed_password):
        return jsonify({'message': 'User added successfully'}), 201
    else:
        return jsonify({'error': 'User already exists'}), 409
    
@app.route('/users', methods=['DELETE'])
def delete_user():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing username and password'}), 400
    if 'username' not in data:
        return jsonify({'error': 'Missing username'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400

    username = data['username']
    password = data['password']

    if database.delete_user(connection, username, password):
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/login', methods=['GET'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing username and password'}), 400
    if 'username' not in data:
        return jsonify({'error': 'Missing username'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400

    username = data['username']
    password = data['password']

    if database.get_user_by_username(username, password, connection):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
