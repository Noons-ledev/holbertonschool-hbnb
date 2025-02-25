#!/usr/bin/python3

"""
Places module for Hbnb project, made by Molly
"""


from .basemodel import BaseModel
from .users import User


class Place(BaseModel):
    """
    Creation of a new place
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        if not isinstance(owner, User):
            raise TypeError("Owner must be user type !")
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        """
        Title given to a place by the owner
        """
        if value is None:
            raise ValueError("Place must have a title !")
        if len(value) > 100:
            raise ValueError("Too long ! 100 characters max !")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """
        Price given to a place by the owner
        """
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
        if not (-180.0 <= value <= 180.0):
            raise ValueError("This longitude seems to be wrong")
        self._longitude = value
