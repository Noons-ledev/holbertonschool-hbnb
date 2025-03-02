#!/usr/bin/python3

"""
Places module for Hbnb project, made by Molly
"""


from .basemodel import BaseModel
from .amenity import Amenity
from .review import Review


class Place(BaseModel):
    """
    Creation of a new place
    """
    def __init__(self, title, description, price, latitude, longitude, owner, amenities):
        from .user import User
        if not isinstance(title, str):
            raise TypeError("Title must be a string!")
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number")
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number")
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number!")
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = amenities

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        """
        Title given to a place by the owner
        """
        if not isinstance(value, str):
            raise TypeError("Title must be a string!")
        if len(value) > 100 or len(value) < 5:
            raise ValueError("Title must be 5 to 100 characters long!")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """
        Price given to a place by the owner
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("You cant enter a negative price")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        Latitude of the place
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("This latitude seems to be wrong")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        Longitude of the place
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number!")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("This longitude seems to be wrong")
        self._longitude = value

    def add_review(self, review):
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    def to_dict(self):
        """Returns only the necessary attributes."""
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description, 
        "price": self.price,
        "latitude": self.latitude,
        "longitude": self.longitude
        }
