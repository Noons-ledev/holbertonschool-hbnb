from app import db
from .basemodel import BaseModel

#Molly : table needed to link place 'n amenity and avoid multiple data duplications
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    """
    Amenity mapping to db
    """

# Molly : Wip 1/2.
# This is my anchor : when u see this, search for the 2/2. This is start and end of my work in progress.

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)  # Unique Amenity Name

    # Many-to-Many Relationship with Place
    places = db.relationship('Place', secondary=place_amenities, back_populates='amenities')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
# Molly : Wip 2/2.
