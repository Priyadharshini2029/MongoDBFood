from flask import Blueprint, request, jsonify
from config.db import connect_db
from pymongo.errors import ServerSelectionTimeoutError
from bson import ObjectId
from datetime import datetime

# Initialize the blueprint for expenses
expenses_blueprint = Blueprint('expenses', __name__)

# Add Expense (POST)
@expenses_blueprint.route('/add', methods=['POST'])
def add_expense():
    try:
        # Get the expense data from the request
        data = request.get_json()
        
        name = data.get('name')
        amount = data.get('amount')
        category = data.get('category')
        date = data.get('date')  # Optional date field (can be passed in the request)

        # If date is not provided, set the current date
        if not date:
            date = datetime.utcnow().isoformat()  # Get the current UTC date and time

        # Validation
        if not name or not amount or not category:
            return jsonify({"message": "All fields are required"}), 400

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')  # Replace with your DB name
            expenses_collection = db.get_collection('expenses')  # Replace with your collection name

            # Create the expense document
            expense_data = {
                "name": name,
                "amount": amount,
                "category": category,
                "date": date  # Add date field to the expense data
            }

            # Insert the new expense into the collection
            result = expenses_collection.insert_one(expense_data)

            # Convert ObjectId to string and return the response
            expense_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string

            # Return success response with the inserted data
            return jsonify({
                "message": "Expense added successfully",
                "expense_id": expense_data["_id"],
                "expense_data": expense_data
            }), 201
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except ServerSelectionTimeoutError as e:
        return jsonify({"message": f"MongoDB connection failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Error adding expense: {str(e)}"}), 500


# Get All Expenses (GET)
@expenses_blueprint.route('/', methods=['GET'])
def get_all_expenses():
    try:
        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')  # Replace with your DB name
            expenses_collection = db.get_collection('expenses')  # Replace with your collection name

            # Retrieve all expenses from the collection
            expenses = expenses_collection.find()

            # Convert the expenses to a list and serialize the ObjectId to string
            expenses_list = []
            for expense in expenses:
                expense["_id"] = str(expense["_id"])  # Convert ObjectId to string
                expenses_list.append(expense)

            return jsonify({
                "message": "Expenses retrieved successfully",
                "expenses": expenses_list
            }), 200
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error retrieving expenses: {str(e)}"}), 500


# Get Expense by ID (GET)
@expenses_blueprint.route('/<expense_id>', methods=['GET'])
def get_expense_by_id(expense_id):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(expense_id):
            return jsonify({"message": "Invalid expense ID"}), 400

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')  # Replace with your DB name
            expenses_collection = db.get_collection('expenses')  # Replace with your collection name

            # Retrieve the expense by ID
            expense = expenses_collection.find_one({"_id": ObjectId(expense_id)})

            if expense:
                expense["_id"] = str(expense["_id"])  # Convert ObjectId to string
                return jsonify({
                    "message": "Expense retrieved successfully",
                    "expense": expense
                }), 200
            else:
                return jsonify({"message": "Expense not found"}), 404
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error retrieving expense: {str(e)}"}), 500


# Update Expense (PUT)
@expenses_blueprint.route('/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(expense_id):
            return jsonify({"message": "Invalid expense ID"}), 400

        # Get the updated data from the request
        data = request.get_json()

        name = data.get('name')
        amount = data.get('amount')
        category = data.get('category')
        date = data.get('date')  # Optional date field

        # If date is not provided, set the current date
        if not date:
            date = datetime.utcnow().isoformat()

        # Validation
        if not name or not amount or not category:
            return jsonify({"message": "All fields are required"}), 400

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')
            expenses_collection = db.get_collection('expenses')

            # Update the expense in the collection
            updated_expense = {
                "name": name,
                "amount": amount,
                "category": category,
                "date": date
            }

            result = expenses_collection.update_one(
                {"_id": ObjectId(expense_id)},
                {"$set": updated_expense}
            )

            if result.matched_count:
                return jsonify({
                    "message": "Expense updated successfully",
                    "updated_expense": updated_expense
                }), 200
            else:
                return jsonify({"message": "Expense not found"}), 404
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error updating expense: {str(e)}"}), 500


# Delete Expense (DELETE)
@expenses_blueprint.route('/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(expense_id):
            return jsonify({"message": "Invalid expense ID"}), 400

        # Connect to the database
        client = connect_db()
        if client:
            db = client.get_database('personal_expenses')
            expenses_collection = db.get_collection('expenses')

            # Delete the expense by ID
            result = expenses_collection.delete_one({"_id": ObjectId(expense_id)})

            if result.deleted_count:
                return jsonify({
                    "message": "Expense deleted successfully"
                }), 200
            else:
                return jsonify({"message": "Expense not found"}), 404
        else:
            return jsonify({"message": "MongoDB connection failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Error deleting expense: {str(e)}"}), 500
