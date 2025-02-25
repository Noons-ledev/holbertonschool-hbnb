#!/usr/bin/python3

"""
Reviews module for Hbnb project, made by Molly
"""


from .basemodel import BaseModel


class Review(BaseModel):
    """
    Creation of a new place
    """
    def __init__(self, text, rating, place, user):
        from .users import User
        from .places import Place
        if not (1 <= rating <= 5) or not isinstance(rating, (int, float)):
            raise ValueError("This must be between 1 and 5 stars")
        if text is None:
            raise ValueError("Please enter a text !")
        if not isinstance(place, Place):
            raise TypeError("place must be a Place object!")
        if not isinstance(user, User):
            raise TypeError("user must be a User!")
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
