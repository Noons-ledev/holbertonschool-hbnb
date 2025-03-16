from app import db

amenity_place = db.Table('amenity_place',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete="CASCADE"), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id', ondelete="CASCADE"), primary_key=True)
)
