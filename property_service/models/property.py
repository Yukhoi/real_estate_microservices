from models.db import db

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    property_type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)  

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "property_type": self.property_type,
            "city": self.city,
            "rooms": self.rooms,
            "owner_id": self.owner_id,
        }
