#!/usr/bin/python3
"""
Users Models made by Noons
"""
from basemodel import BaseModel
import re

def validate_email(mail):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_regex, mail):
        return mail
    raise ValueError("Mail format not accepted")

def validate_names(name):
    if not isinstance(name, str):
        raise TypeError("Names must be strings")
    forbidenchars = "0123456789/\\\"?!@#&\'()§$*`£%=+:,¥€[{]};_"
    for char in forbidenchars:
        if char in name or len(name) > 50:
            raise ValueError("Names must contain letters only and be "
                            "50 characters maximum")
    return name


class User(BaseModel):


    def __init__(self, first_name, last_name, email, password, isadmin=False):
        super().__init__()
        self.first_name = validate_names(first_name)
        self.last_name = validate_names(last_name)
        self.isadmin = isadmin
        self.email = validate_email(email)
        self.password = password
        self.places = []

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.__password = value

    @property
    def isadmin(self):
        return self.__isadmin

    @isadmin.setter
    def isadmin(self, value):
        if isinstance(value, bool):
            self.__isadmin = value
        else:
            raise ValueError("IsAdmin can be True or false only")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        check = validate_email(value)
        if check == value:
            self.__email = value
        else:
            raise ValueError("Email must be from a valid format")


#Here we are putting as private attribute first and last name,
#So that the User can't modify those value without the validate_name check
    @property
    def  first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        check = validate_names(value)
        if check == value:
            self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        check = validate_names(value)
        if check == value:
            self.__last_name = value