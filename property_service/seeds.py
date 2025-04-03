from app import create_app
from models.property import Property
from models.db import db

app = create_app()

with app.app_context():
    db.drop_all()
    print("Dropped existing tables.")

    db.create_all()
    print("Created tables.")

    properties = [
        Property(
            name="Cozy Apartment",
            description="A cozy apartment in the city center.",
            property_type="Apartment",
            city="New York",
            rooms=2,
            owner_id=1
        ),
        Property(
            name="Luxury Villa",
            description="A luxurious villa with a private pool.",
            property_type="Villa",
            city="Los Angeles",
            rooms=5,
            owner_id=2
        ),
        Property(
            name="Beach House",
            description="A beautiful beach house with ocean views.",
            property_type="House",
            city="Miami",
            rooms=3,
            owner_id=3
        ),
        Property(
            name="Modern Studio",
            description="A modern studio apartment perfect for singles.",
            property_type="Studio",
            city="San Francisco",
            rooms=1,
            owner_id=4
        ),
    ]

    db.session.bulk_save_objects(properties)
    db.session.commit()
    print("Inserted seed properties.")