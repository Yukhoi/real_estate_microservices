from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/login", methods=["POST"])(AuthController.login)
auth_bp.route("/verify", methods=["GET"])(AuthController.verify_token)
