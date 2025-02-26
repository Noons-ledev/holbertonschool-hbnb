from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
# from app.api.v1.amenity import api as amenity_ns
# from app.api.v1.review import api as review_ns


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    # api.add_namespace(amenity_ns, path='/api/v1/amenity')
    # api.add_namespace(review_ns, path='/api/v1/review')
    return app