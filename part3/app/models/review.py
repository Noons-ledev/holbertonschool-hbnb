from app import db
from .basemodel import BaseModel

class Review(BaseModel):
    """
    Review model mapped to the 'reviews' table in the database
    """

# Molly : Wip 1/2.
# This is my anchor : when u see this, search for the 2/2. This is start and end of my work in progress.

    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)  # Review content (max 500 chars)
    rating = db.Column(db.Integer, nullable=False)  # Rating from 1 to 5

    # Foreign Keys : each review is linked to existing place, and is user

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships between reviews and other models

    place = db.relationship('Place', back_populates='reviews', foreign_keys='Review.place_id')
    user = db.relationship('User', back_populates='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        }
# Molly : Wip 2/2.