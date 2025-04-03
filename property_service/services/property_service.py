import requests
from models.property import Property
from models.room import Room
from models.db import db
from sqlalchemy.orm import joinedload


class PropertyService:

    @staticmethod
    def search_property(city, token):
        
        user_information = PropertyService.verify_token(token)

        if "error" in user_information:
            return user_information, 403
        
        user_city = user_information.get("city")

        if user_city:
            if user_city.lower() != city.lower():
                return {"error": f"You can only view properties in {user_city}"}, 403
        else:
            bind_city_response, status_code = PropertyService.bind_city_to_user(user_id, city)
            if status_code != 200:
                return {"error": "Failed to bind city"}, 500

        properties = Property.query.options(joinedload(Property.rooms)).filter_by(city=city).all()
        if not properties:
            return {"error": "No properties found"}, 404

        result = []
        for property in properties:
            property_dict = property.to_dict()
            property_dict["rooms"] = [room.to_dict() for room in property.rooms]
            result.append(property_dict)

        return result, 200
        
    @staticmethod
    def update_property(property_id, property_data, token):
        
        user_information = PropertyService.verify_token(token)

        if "error" in user_information:
            return user_information, 403
        
        property = Property.query.get(property_id)
        if not property:
            return {"error": "Property not found"}, 404
        
        if property.owner_id != user_information.get("id"):
            return {"error": "You do not have permission to update this property"}, 403
        
        if "name" in property_data:
            property.name = property_data.get("name", property.name)
        if "description" in property_data:
            property.description = property_data.get("description", property.description)
        if "property_type" in property_data:        
            property.property_type = property_data.get("property_type", property.property_type)
        if "city" in property_data:
            property.city = property_data.get("city", property.city)

        if "rooms" in property_data:
          for room_data in property_data["rooms"]:
              room_id = room_data.get("id")
              if room_id:
                  room = Room.query.get(room_id)
                  if room and room.property_id == property_id:
                      room.name = room_data.get("name", room.name)
                      room.size = room_data.get("size", room.size)
              else:
                  new_room = Room(
                      name=room_data["name"],
                      size=room_data["size"],
                      property_id=property_id
                  )
                  db.session.add(new_room)

        db.session.commit()
        return property.to_dict(), 200
    
    @staticmethod
    def create_property(property_data, token):
        user_information = PropertyService.verify_token(token)

        if "error" in user_information:
            return user_information, 403
        
        property = Property(
            name=property_data.get("name"),
            description=property_data.get("description"),
            property_type=property_data.get("property_type"),
            city=property_data.get("city"),
            owner_id=user_information.get("id")
        )

        new_property = Property(
          name=property_data.get("name"),
          description=property_data.get("description"),
          property_type=property_data.get("property_type"),
          city=property_data.get("city"),
          owner_id=user_information.get("id")
        )

        db.session.add(new_property)
        db.session.flush()
        
        if "rooms" in property_data:
          for room_data in property_data["rooms"]:
              new_room = Room(
                  name=room_data.get("name"),
                  size=room_data.get("size"),
                  property_id=new_property.id
              )
              db.session.add(new_room)

        db.session.commit()
        
        return new_property.to_dict(), 201 
       
    @staticmethod
    def verify_token(token):
        user_service_url = f"http://auth_service:5002/auth/verify"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(user_service_url, headers=headers)
        if response.status_code == 200:
            print(f"Token verified successfully: {response.json()}", flush=True)
            response_data = response.json()
            return response_data.get("user", {})
        return {"error": "Token invalid"}

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
