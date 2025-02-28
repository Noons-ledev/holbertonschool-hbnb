#!/usr/bin/python3
import uuid
"""
Reviews module for Hbnb project, made by Molly
"""


from .basemodel import BaseModel


class Review(BaseModel):
    """
    Creation of a new place
    """
    def __init__(self, text, rating, place_id, user_id):
        from .user import User
        from .place import Place
        if not (1 <= rating <= 5) or not isinstance(rating, (int, float)):
            raise ValueError("This must be between 1 and 5 stars")
        if text is None:
            raise ValueError("Please enter a text !")
        if not isinstance(place_id, uuid):
            raise TypeError("place must be a Place object!")
        if not isinstance(user_id, uuid):
            raise TypeError("user must be a User!")
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id