from app import create_app
from models.property import Property
from models.room import Room
from models.db import db

app = create_app()

with app.app_context():
    db.drop_all()
    print("Dropped existing tables.")

    db.create_all()
    print("Created tables.")

    properties = [
        Property(name="Charming Loft", description="A cozy loft in central Paris.", property_type="Apartment", city="Paris", owner_id=1),
        Property(name="Eiffel Tower View", description="An apartment with a stunning Eiffel Tower view.", property_type="Apartment", city="Paris", owner_id=2),

        Property(name="Riverside Villa", description="A luxurious villa near the Rhône River.", property_type="Villa", city="Lyon", owner_id=1),
        Property(name="Modern Flat", description="A modern apartment close to public transport.", property_type="Apartment", city="Lyon", owner_id=3),

        Property(name="Seaside House", description="A beautiful house overlooking the Mediterranean.", property_type="House", city="Marseille", owner_id=4),

        Property(name="Wine Estate", description="A vineyard estate in the Bordeaux region.", property_type="Estate", city="Bordeaux", owner_id=2),
        Property(name="Downtown Studio", description="A compact studio in the heart of Bordeaux.", property_type="Studio", city="Bordeaux", owner_id=5),

        Property(name="Historic Townhouse", description="A traditional Alsace-style house.", property_type="Townhouse", city="Strasbourg", owner_id=3),
    ]

    db.session.bulk_save_objects(properties)
    db.session.commit()
    print("Inserted seed properties.")

    properties = Property.query.all()

    rooms = [
        Room(name="Living Room", size=30, property_id=properties[0].id),
        Room(name="Master Bedroom", size=20, property_id=properties[0].id),
        Room(name="Balcony", size=10, property_id=properties[1].id),
        Room(name="Guest Room", size=18, property_id=properties[1].id),

        Room(name="Swimming Pool", size=50, property_id=properties[2].id),
        Room(name="Dining Room", size=25, property_id=properties[2].id),
        Room(name="Bedroom", size=20, property_id=properties[3].id),

        Room(name="Seaview Room", size=35, property_id=properties[4].id),
        Room(name="Garden Room", size=28, property_id=properties[4].id),

        Room(name="Wine Cellar", size=40, property_id=properties[5].id),
        Room(name="Tasting Room", size=30, property_id=properties[5].id),
        Room(name="Compact Living", size=22, property_id=properties[6].id),

        Room(name="Attic Room", size=25, property_id=properties[7].id),
        Room(name="Historic Dining", size=35, property_id=properties[7].id),
    ]

    db.session.bulk_save_objects(rooms)
    db.session.commit()
    print("Inserted seed rooms.")
