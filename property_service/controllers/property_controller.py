from flask import Blueprint, jsonify, request
from services.property_service import PropertyService

class PropertyController:
    def __init__(self, property_service):
        self.property_service = property_service

    def create_property(self, property_data):
        return self.property_service.create_property(property_data)

    @staticmethod
    def search_property():
        user_id = request.args.get("user_id", type=int)
        city = request.args.get("city", type=str)

        if not user_id or not city:
            return jsonify({"error": "User ID and city are required"}), 400

        response, status_code = PropertyService.search_property(city, user_id)
        return jsonify(response), status_code


    def update_property(self, property_id, property_data):
        return self.property_service.update_property(property_id, property_data)

    def delete_property(self, property_id):
        return self.property_service.delete_property(property_id)