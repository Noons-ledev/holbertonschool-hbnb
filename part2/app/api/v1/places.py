from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities

user_model = api.model('PlaceUser', {
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String(required=True, description='List of amenities')),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

place_creation_model = api.model('place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String(required=True, description='List of amenities')),
})
place_update_model = api.model('update', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String(required=True, description='List of amenities')),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_creation_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Registration of a new place - Molly & Noons
        data = api.payload
        if not data: 
            return {"error": "No data provided"}, 400
        check = False
        user_id = data.get('owner')
        if not user_id:
            return {"error": "User ID required"}, 400
        userlist = facade.get_users_list()
        check = any(user.get("id") == user_id for user in userlist)
        if not check:
            return {'Error': 'No valid ID provided'}, 400
        try:
            new_place = facade.create_place(data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "amenities": [(facade.get_amenity(amenity).to_dict()) for amenity in new_place.amenities]
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        #  Molly 
        places = facade.get_all_places()

        if not places:
            return {'error': "not found"}, 400
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Molly
        try:
            place = facade.get_place(place_id)
            owner_id = place.owner
            owner_info = facade.get_user(owner_id)
            reviews_list = [{"id": r.id, "text" : r.text, "rating": r.rating, "uder_id": r.user_id, "place_id": r.place_id} for r in place.reviews]
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": owner_info.to_dict(),
                "amenities": [(facade.get_amenity(amenity).to_dict()) for amenity in place.amenities],
                "reviews": reviews_list
            }, 200
        except Exception as e:
            return {"error": str(e)}, 404

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        data = api.payload

        if not data:
            return {"error": "No data provided"}, 400
        if data.get('owner') is not None:
            return {'error' : 'No owner informations allowed'}
        if data.get('id') is not None:
            return {'error': 'No ID allowed in data'}, 400
        try:
            facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

