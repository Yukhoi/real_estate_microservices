from flask import Blueprint
from controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)

user_bp.route("/register", methods=["POST"])(UserController.register)

user_bp.route('/<int:user_id>', methods=['GET'])(UserController.get_user)

user_bp.route('/<int:user_id>', methods=['PUT'])(UserController.update_user)

user_bp.route('/<int:user_id>', methods=['DELETE'])(UserController.delete_user)

user_bp.route('/<int:user_id>/bind_city', methods=['POST'])(UserController.bind_city)