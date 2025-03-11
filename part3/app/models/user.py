from app import db, bcrypt
from .basemodel import BaseModel
import re

class User(BaseModel):

# Molly : Wip 1/2.
# This is my anchor : when u see this, search for the 2/2. This is start and end of my work in progress.

    __tablename__ = 'users'

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password = db.Column("password", db.String(128), nullable=False)
    _is_admin = db.Column("is_admin", db.Boolean, default=False)

#Molly : password handling

    @property
    def password(self):
            raise AttributeError("Password can't be shown")

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

# Molly's note : need to implement db.relationship  in models to, for each

    reviews = db.relationship('Review', back_populates='user', lazy='dynamic') #one user can write multiple reviews
    places = db.relationship('Place', back_populates='owner', lazy='dynamic') #one user can own multiple places

# First name

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length('First name', value, 50)
        self.__first_name = value

# Laste name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length('Last name', value, 50)
        self.__last_name = value

# Mail
# Some changes : SQLAlchemy handle "unicity", every data must be unique. Impossible to have 2 account with the same mail

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value): #Molly : re.match is a func used to check if mail is ok regex
            raise ValueError("Invalid email format")
        self._email = value

# Admin

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self.__is_admin = value

# Convert to dictionnary

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

#Molly : Wip 2/2
