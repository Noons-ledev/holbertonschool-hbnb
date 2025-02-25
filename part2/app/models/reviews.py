#!/usr/bin/python3

"""
Reviews module for Hbnb project, made by Molly
"""


from .basemodel import BaseModel
from .users import User
from .places import Place


class Reviews(BaseModel):
    """
    Creation of a new place
    """
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not (1 <= rating <= 5):
            raise ValueError("This must be between 1 and 5 stars")
        if text is None:
            raise ValueError("Please enter a text !")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
