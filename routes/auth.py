from flask import Blueprint, request, jsonify
from config.db import connect_db
import bcrypt
import jwt
from datetime import datetime, timedelta

auth_blueprint = Blueprint('auth', __name__)

# User Registration (POST)
@auth_blueprint.route('/register', methods=['POST'])
def register():
    try:
        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate the data
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')  # Replace with your DB name
            users_collection = db.get_collection('users')  # Replace with your collection name

            # Check if the username already exists
            existing_user = users_collection.find_one({"username": username})
            if existing_user:
                return jsonify({"message": "Username already exists"}), 400

            # Insert the new user into the database
            user_data = {
                "username": username,
                "password": hashed_password
            }
            users_collection.insert_one(user_data)

            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500


# User Login (POST)
@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate the data
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')  # Replace with your DB name
            users_collection = db.get_collection('users')  # Replace with your collection name

            # Find the user by username
            user = users_collection.find_one({"username": username})

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Create a JWT token
                token = jwt.encode(
                    {"username": username, "exp": datetime.utcnow() + timedelta(hours=1)},
                    'secret_key', algorithm='HS256'
                )

                return jsonify({"message": "Login successful", "token": token}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error logging in: {str(e)}"}), 500
