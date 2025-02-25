#!/usr/bin/python3
"""
Amenities Models made by Noons
"""
from basemodel import BaseModel

class Amenities(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
