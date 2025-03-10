from app import db
import uuid
from datetime import datetime
from sqlalchemy.sql import func


class BaseModel:
    def __init__(self):
        __abstract__ = True

        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        created_at = db.Column(db.DateTime, default=func.now())
        updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

        #Molly : utcnow isnt used naymore. We could replace it by func.now, sqlalchemy will handle everything

    def save(self):
        self.updated_at = func.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

#Molly : changing these two for a static method, because they dont need self

    @staticmethod
    def is_max_length(name, value, max_length):
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.")

    @staticmethod
    def is_between(name, value, min, max):
        if not min < value < max:
            raise ValueError(f"{name} must be between {min} and {max}.")
