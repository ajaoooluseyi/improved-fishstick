from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import uuid

# import docker

app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["usersdb"]
collection = db["users"]

# Update Docker API version DOCKER_API_VERSION = '1.41'

# Create Docker client docker_client = docker.DockerClient(version=DOCKER_API_VERSION)


class UserResource(Resource):
    def get(self, user_id):
        user = collection.find_one({"id": user_id})
        if user:
            serialized_user = [{**user, "_id": str(user["_id"])}]
            return serialized_user, 200

        else:
            return {"message": "User not found"}, 404

    def put(self, user_id):
        user_data = request.get_json()
        updated_user = {
            "name": user_data["name"],
            "email": user_data["email"],
            "password": user_data["password"],
        }
        result = collection.update_one({"id": user_id}, {"$set": updated_user})
        if result.modified_count == 1:
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    def delete(self, user_id):
        result = collection.delete_one({"id": user_id})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404


class UserListResource(Resource):
    def get(self):
        users = list(collection.find())
        serialized_users = [{**user, "_id": str(user["_id"])} for user in users]
        print(serialized_users)
        return serialized_users, 200

    def post(self):
        user_data = request.get_json()
        print(user_data)
        new_user = {
            "id": str(uuid.uuid4()),
            "name": user_data["name"],
            "email": user_data["email"],
            "password": user_data["password"],
        }
        result = collection.insert_one(new_user)
        return {
            "message": "User created successfully",
            "user_data_id": str(result.inserted_id),
        }, 201


api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<string:user_id>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
