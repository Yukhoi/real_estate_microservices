from flask import jsonify, request
from middlewares.user_middleware import validate_body
from services.user_service import UserService
from werkzeug.exceptions import NotFound

class UserController:
    
    @staticmethod
    def get_user(user_id):
        try:
          user = UserService.get_user_by_id(user_id)
          return jsonify({
              "first_name": user.first_name,
              "last_name": user.last_name,
              "birth_date": user.birth_date,
              "city": user.city
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
    @validate_body(['first_name', 'last_name', 'birth_date','email', 'password'])
    def register():
        data = request.get_json()
        if UserService.get_user_by_email(data.get('email')):
            return jsonify({"message": "Email already exists"}), 400
        user = UserService.create_user(data)
        return jsonify({"message": "User created", "id": user.id}), 201
    
    @staticmethod
    @validate_body(['city'])
    def bind_city(user_id):
        data = request.get_json()
        city = data.get('city')

        print(f"Binding city {city} to user {user_id}", flush=True)
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        print(f"Binding city {city} to user {user_id}", flush=True)
        
        update_data = {"city": city}
        UserService.update_user(user_id, update_data)
        
        return jsonify({"message": "City bound successfully", "user_id": user.id}), 200
    
    