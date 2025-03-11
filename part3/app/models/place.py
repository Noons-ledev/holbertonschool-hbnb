from app import db
from .basemodel import BaseModel

class Place(BaseModel):
    """
    Place model mapping
    """
# Molly : Wip 1/2.
# This is my anchor : when u see this, search for the 2/2. This is start and end of my work in progress.

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Foreign Key for the owner to link to place
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships between other models
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', lazy='dynamic')

    def to_dict(self):
        """
        Convert place instance to dictionary format
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }

    def to_dict_list(self):
        """
        Convert place with relationships into a dictionary format
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'reviews': [review.to_dict() for review in self.reviews.all()]
        }
# Molly : Wip 2/2.
