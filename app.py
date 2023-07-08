from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["user_database"]
collection = db["users"]


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }


def user_from_dict(user_dict):
    return User(
        name=user_dict["name"],
        email=user_dict["email"],
        password=user_dict["password"],
    )


# Get all users
@app.route("/users", methods=["GET"])
def get_all_users():
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)


# Get a user by ID
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user = collection.find_one({"_id": ObjectId(str(id))})
    if user:
        user["_id"] = str(user["_id"])
        return json.dumps(user, default=str)
    else:
        return jsonify({"error": "User not found"}), 404


# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.get_json()
    if (
        "name" not in user_data
        or "email" not in user_data
        or "password" not in user_data
    ):
        return jsonify({"error": "Missing required fields"}), 400
    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password=user_data["password"],
    )
    user_dict = user.to_dict()
    user_id = collection.insert_one(user_dict).inserted_id
    user_dict["_id"] = str(user_id)
    return jsonify(user_dict)


# Update a user by ID
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user_data = request.get_json()
    if (
        "name" not in user_data
        or "email" not in user_data
        or "password" not in user_data
    ):
        return jsonify({"error": "Missing required fields"}), 400
    result = collection.update_one({"_id": ObjectId(str(id))}, {"$set": user_data})
    if result.modified_count:
        user = collection.find_one({"_id": ObjectId(str(id))})
        user["_id"] = str(user["_id"])
        return json.dumps(user, default=str)
    else:
        return jsonify({"error": "User not found"}), 404


# Delete a user by ID
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = collection.delete_one({"_id": ObjectId(str(id))})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run()
