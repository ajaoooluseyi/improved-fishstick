from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["user_database"]
collection = db["users"]


class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }


def user_from_dict(user_dict):
    return User(
        id=user_dict["_id"],
        name=user_dict["name"],
        email=user_dict["email"],
        password=user_dict["password"],
    )


# Get all users
@app.route("/users", methods=["GET"])
def get_all_users():
    users = []
    for user_dict in collection.find():
        user = user_from_dict(user_dict)
        users.append(user.to_dict())
    return jsonify(users)


# Get a user by ID
@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    user_dict = collection.find_one({"_id": ObjectId(id)})
    if user_dict:
        user = user_from_dict(user_dict)
        return jsonify(user.to_dict())
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
    user = User(None, user_data["name"], user_data["email"], user_data["password"])
    user_dict = user.to_dict()
    user_id = collection.insert_one(user_dict).inserted_id
    user.id = str(user_id)
    return jsonify(user.to_dict())


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
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": user_data})
    if result.modified_count:
        user_dict = collection.find_one({"_id": ObjectId(id)})
        user = user_from_dict(user_dict)
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404


# Delete a user by ID
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run()
