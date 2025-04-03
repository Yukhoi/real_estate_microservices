from flask import jsonify, request
import requests
from models.property import Property


class PropertyService:

    @staticmethod
    def search_property(city, user_id):
        print(f"Searching properties in {city} for user {user_id}", flush=True)
        user_city = PropertyService.get_user_city(user_id)
        if user_city:
            if user_city.lower() != city.lower():
                return {"error": f"You can only view properties in {user_city}"}, 403
        else:
            bind_city_response, status_code = PropertyService.bind_city_to_user(user_id, city)
            if status_code != 200:
                return {"error": "Failed to bind city"}, 500

        properties = Property.query.filter_by(city=city).all()
        if not properties:
            return {"error": "No properties found"}, 404

        return [property.to_dict() for property in properties], 200

    @staticmethod
    def get_user_city(user_id):
        user_service_url = f"http://user_service:5001/users/{user_id}"
        response = requests.get(user_service_url)
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("city")
        return None, 404

    @staticmethod
    def bind_city_to_user(user_id, city):
        update_url = f"http://user_service:5001/users/{user_id}/bind_city"
        update_response = requests.post(update_url, json={"city": city})
        if update_response.status_code != 200:
            return {"error": "Failed to bind city"}, 500
        return {"message": "City bound successfully"}, 200
