import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth import auth_blueprint
from routes.expenses import expenses_blueprint
from config.db import connect_db

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

@app.route('/')
def index():
    client = connect_db()  # MongoDB connection check
    if client:
        return jsonify({"message": "MongoDB is connected"})
    else:
        return jsonify({"message": "MongoDB connection failed"}), 500

# Register Blueprints for authentication and expenses routes
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(expenses_blueprint, url_prefix='/api/expenses')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app on port 5000
