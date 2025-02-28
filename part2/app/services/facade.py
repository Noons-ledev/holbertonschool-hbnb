#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from ..models.place import Place
from ..models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        from ..models.user import User
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_users_list(self):
        list = self.user_repo.get_all()
        user_list = [user.to_dict() for user in list]
        return  user_list

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)


    def create_amenity(self, amenity_data):
        from ..models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        list = self.amenity_repo.get_all()
        amenity_list = [amenity.to_dict() for amenity in list]
        return  amenity_list

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def create_place(self, place_data):
        # Molly - logic to create a place, including validation for price, latitude, and longitude
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Molly - logic to retrieve a place by ID, including associated owner and amenities
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place do not exist !")
        return place

    def get_all_places(self):
        # Molly - retrieve all places
        list = self.place_repo.get_all()
        place_list = [place.to_dict() for place in list]
        return  place_list

    def update_place(self, place_id, place_data):
        # Molly - update a place
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
    # Molly - logic to create a review, including validation for user_id, place_id, and rating
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        #  for logic to retrieve a review by ID
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        #  for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        #  for logic to retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute('place', place_id)


    def update_review(self, review_id, review_data):
        #  for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        #  for logic to delete a review
        return self.review_repo.delete(review_id)