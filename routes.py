from flask import Flask, request, jsonify
import database
import helpers 

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
        return jsonify({'error': 'User already exists'}), 400
