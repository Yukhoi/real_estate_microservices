from flask import Blueprint, jsonify, request
from services.property_service import PropertyService
from flask_jwt_extended import jwt_required, get_jwt_identity

class PropertyController:
    def __init__(self, property_service):
        self.property_service = property_service

    def create_property(self, property_data):
        return self.property_service.create_property(property_data)

    @staticmethod
    def search_property():
        city = request.args.get("city", type=str)

        token = request.headers.get("Authorization").split()[1]
        if not token:
            return jsonify({"error": "JWT token is required"}), 401

        if not city:
            return jsonify({"error": "city are required"}), 400

        response, status_code = PropertyService.search_property(city, token)
        return jsonify(response), status_code

    @staticmethod
    def update_property(property_id):
        token = request.headers.get("Authorization").split()[1]
        if not token:
            return jsonify({"error": "JWT token is required"}), 401

        property_data = request.get_json()
        if not property_data:
            return jsonify({"error": "Property data is required"}), 400
        
        response, status_code = PropertyService.update_property(property_id, property_data, token)
        return jsonify(response), status_code
    
    @staticmethod
    def create_property():
        token = request.headers.get("Authorization").split()[1]
        if not token:
            return jsonify({"error": "JWT token is required"}), 401

        property_data = request.get_json()
        if not property_data:
            return jsonify({"error": "Property data is required"}), 400
        
        response, status_code = PropertyService.create_property(property_data, token)
        return jsonify(response), status_code
        
        
