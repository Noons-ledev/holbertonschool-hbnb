from app import db
from .basemodel import BaseModel
from .review import Review
from .user import User
from .amenity import Amenity


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
    amenities = db.relationship("Amenity", secondary="place_amenity", back_populates="places")

    # Relationships between other models
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', foreign_keys='Review.place_id', cascade="all, delete-orphan")

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self.__title = value

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        self.__price = value

    @property
    def latitude(self):
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be a float")
        super().is_between("latitude", value, -90, 90)
        self.__latitude = value
    
    @property
    def longitude(self):
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Longitude must be a float")
        super().is_between("longitude", value, -180, 180)
        self.__longitude = value

    def add_review(self, review):
        """Add a review to the place."""
        if not isinstance(review, Review):
            raise TypeError("Expected a Review object")
        
        session = db.session.object_session(self) or db.session

        if review not in session:
            session.add(review)
            session.flush()

        with db.session.no_autoflush:
            if review not in self.reviews:
                review.place = self
                self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected an Amenity object")

        session = db.session.object_session(self) or db.session

        with db.session.no_autoflush:
            if amenity not in self.amenities:
                if amenity not in session:
                    session.add(amenity)
                    session.flush()
                self.amenities.append(amenity)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id
        }
    
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': self.amenities,
            'reviews': self.reviews
        }