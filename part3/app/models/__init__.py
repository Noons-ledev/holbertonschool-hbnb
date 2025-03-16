from app import db
Base = db.Model

from app.models.user import User
from app.models.place import Place
from app.models.amenity_place import amenity_place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.basemodel import BaseModel

