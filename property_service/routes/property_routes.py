from flask import Blueprint
from controllers.property_controller import PropertyController

property_bp = Blueprint("property", __name__)

property_bp.route("/search", methods=["GET"])(PropertyController.search_property)
