#!/usr/bin/python3
"""
Amenities Models made by Noons
"""
from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string!")
        if len(name) > 50:
            raise ValueError("Name length must be 50 characters maximum!")
        super().__init__()
        self.name = name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}