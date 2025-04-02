from flask import jsonify, request
from middlewares.user_middleware import validate_body
from services.user_service import UserService
from werkzeug.exceptions import NotFound

class UserController:
    
    @staticmethod
    @validate_body(['first_name', 'last_name', 'birth_date'])
    def create_user():
        data = request.get_json()
        user = UserService.create_user(data)
        return jsonify({"message": "User created", "id": user.id}), 201
    
    @staticmethod
    def get_user(user_id):
        try:
          user = UserService.get_user_by_id(user_id)
          return jsonify({
              "first_name": user.first_name,
              "last_name": user.last_name,
              "birth_date": user.birth_date
          }), 200
        except NotFound:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404
    
    @staticmethod
    def update_user(user_id):
        try:
            data = request.get_json()
            updated_id = UserService.update_user(user_id, data)
            return jsonify({
                "message": "User updated successfully",
                "user_id": updated_id
            }), 200
        except NotFound:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404

    @staticmethod
    def delete_user(user_id):
        try:
            deleted_id = UserService.delete_user(user_id)
            return jsonify({
                "message": f"User with ID {deleted_id} deleted successfully"
            }), 200
        except NotFound:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404
        
    @staticmethod
    def register():
        data = request.get_json()
        if UserService.get_user_by_email(data.get('email')):
            return jsonify({"message": "Email already exists"}), 400
        user = UserService.create_user(data)
        return jsonify({"message": "User created", "id": user.id}), 201
    
    