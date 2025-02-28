from flask_restx import Namespace, Resource, fields
from app.services import facade
api = Namespace('reviews', description='Review operations')
# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # The logic to register a new review
        data = api.payload
        if not data:
            return {"error" : "No data provided"}, 400
        try:
            new_review = facade.create_review(data)
            return { # Molly - Or, return new_review. to_dict(), 201 ?? + in model / user, add a to dict function
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 201
        except ValueError:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Molly - logic to return a list of all reviews
        reviews = facade.get_all_reviews()
        if not reviews:
            return {"message": "No reviews found"}, 200
        result = []
        for review in reviews:
            result.append({
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
            })
        return result, 200
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Molly - logic to retrieve a review by ID
        if not review_id.isalnum():  # UUID check
            return {"error": "Invalid review ID"}, 400
        obj = facade.get_review(review_id)
        if not obj:
            return {"error": "Review not found"}, 404
        return {
            "id": obj.id,
            "text": obj.text,
            "rating": obj.rating,
            "place_id": obj.place_id,
            "user_id": obj.user_id
        }, 200 #Molly if la review exist, return dict json
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Molly - logic to update a review by ID
        data = api.payload
        if not data:
            return {"error": "No data provided"}, 400
        try:
            review, message, status_code = facade.update_review(review_id, data)
            if status_code == 404:
                return {"error": "Review not found"}, 404
            return {"message": "Review updated successfully"}, 200
        except ValueError:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Molly -  logic to delete a review
        review, message, status_code = facade.delete_review(review_id)

        if status_code == 404:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Molly -  return a list of reviews for a place
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None: #Molly if place exist, but as no reviews, do not return 404 but 200 w empty list
            return {"error": "place not found"}, 404
        return [{"id": review.id, "text": review.text, "rating": review.rating} for review in reviews], 200