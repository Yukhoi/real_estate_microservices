from flask import Blueprint
from controllers.property_controller import PropertyController

property_bp = Blueprint("property", __name__)

property_bp.route("/search", methods=["GET"])(PropertyController.search_property)

property_bp.route("/update/<int:property_id>", methods=["PUT"])(PropertyController.update_property)

property_bp.route("/create", methods=["POST"])(PropertyController.create_property)
