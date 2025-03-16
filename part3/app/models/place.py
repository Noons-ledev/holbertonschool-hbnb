from sqlalchemy.orm import relationship
from app import db
from .baseclass import BaseModel
from app.models.user import User
from app.models.amenity_place import amenity_place


class Place(BaseModel):
    __tablename__ = "places"

    _title = db.Column(db.String(100), nullable=False)
    _description = db.Column(db.String(300), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True, nullable=False)
    reviews = db.relationship('Review', backref=db.backref('review', lazy=True), lazy='subquery', cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=amenity_place, backref=db.backref('places', lazy=True), lazy='subquery', cascade="all, delete")


    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self._title = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        super().is_between("latitude", value, -90, 90)
        self._latitude = value
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        super().is_between("longitude", value, -180, 180)
        self._longitude = value

    @property
    def owner(self):
        return self._owner_id
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a user instance")
        self._owner_id = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
        db.session.commit()
    
    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)
        db.session.commit()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self._title,
            'description': self._description,
            'price': self._price,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'owner_id': self._owner_id
        }
    
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self._title,
            'description': self._description,
            'price': self._price,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'owner_id': self._owner_id,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews': [review.to_dict() for review in self.reviews]
        }