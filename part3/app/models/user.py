
from .baseclass import BaseModel
from app import db
import re


class User(BaseModel):
    emails = set()
    __tablename__ = 'user'

    _first_name = db.Column(db.String(50), nullable=False)
    _last_name = db.Column(db.String(50), nullable=False)
    _email = db.Column(db.String(120), nullable=False, unique=True)
    _password = db.Column(db.String(128), nullable=False)
    review = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")
    place = db.relationship('Place', backref='user', lazy=True, cascade="all, delete-orphan")
    _is_admin = db.Column(db.Boolean, default=False)

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length('First name', value, 50)
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length('Last name', value, 50)
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        if value in User.emails:
            raise ValueError("Email already exists")
        if hasattr(self, "_User_email"):
            User.emails.discard(self._email)
        self._email = value
        User.emails.add(value)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        self._password = self.hash_password(value)

    @property
    def is_admin(self):
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self._is_admin = value

    def add_place(self, place):
        """Add an amenity to the place."""
        self.place.append(place)
        db.session.commit()

    def add_review(self, review):
        """Add an amenity to the place."""
        self.reviews.append(review)
        db.session.commit()

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)
        db.session.commit()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self._password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
