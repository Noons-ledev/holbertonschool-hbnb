import unittest
import uuid
from app.models.user import User
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository
from app import create_app
from flask import json


class TestUserAPI(unittest.TestCase):
    """
    Unit tests for the User API.

    === Setup ===
        - setUp(self): Initializes the HBnBFacade and creates a test user.

    === Testing user creation ===
        - test_01_create_user_success(self): Valid user creation.
        - test_02_create_user_missing_fields(self): Missing required fields.
        - test_03_create_user_duplicate_email(self): Attempt to create a user with an already used email.

    === Testing get_user method ===
        - test_04_get_all_users(self): Retrieve all users.
        - test_05_get_user_success(self): Retrieve a user by ID.
        - test_06_get_user_not_found(self): Retrieve a user with an invalid/non-existent ID.

    === Testing update_user method ===
        - test_07_update_user_success(self): Updating user with valid data.
        - test_08_update_user_invalid_fields(self): Updating user with invalid fields (e.g., malformed email).
        - test_09_update_user_duplicate_email(self): Attempt to update a user's email with one that is already used.
    """

    def setUp(self):
        """Setup for each test."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()
        self.facade.user_repo = InMemoryRepository()

        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        # Créer un utilisateur pour les tests
        self.test_user = self.facade.create_user(self.user_data)

    def test_01_create_user_success(self):
        """Test creating a valid user."""
        user_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        }
        user = self.facade.create_user(user_data)
        self.assertIsInstance(user.id, str)
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.email, "alice.smith@example.com")

    def test_02_create_user_missing_fields(self):
        """Test creating a user with missing fields."""
        incomplete_user_data = {"first_name": "Alice"}  # Données manquantes (par exemple, pas de 'email')
        with self.assertRaises(ValueError):
            self.facade.create_user(incomplete_user_data)

    def test_03_create_user_duplicate_email(self):
        """Test créer un utilisateur avec un email déjà utilisé."""
    
    # Créer un premier utilisateur avec un email
        response = self.client.post('/api/v1/users/', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    # Tenter de créer un second utilisateur avec le même email
        response = self.client.post('api/v1/users/', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 409)  # Attendu 409 pour conflit

        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], "Email already registered")

    def test_04_get_all_users(self):
        """Test retrieving all users."""
        self.facade.create_user({"first_name": "Alice", "last_name": "Brown", "email": "alice@example.com"})
        self.facade.create_user({"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com"})

        users = self.facade.get_users_list()
        self.assertEqual(len(users), 3) 

    def test_05_get_user_success(self):
        """Test retrieving a valid user."""
        user = self.facade.get_user(self.test_user.id)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.email, "john.doe@example.com")

    def test_06_get_user_not_found(self):
        """Test retrieving a non-existent user."""
        non_existent_id = str(uuid.uuid4())  # Utiliser un ID qui n'existe pas
        response = self.client.get(f'/api/v1/users/{non_existent_id}')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], "User not found")


    def test_07_update_user_success(self):
        """Test updating a user with valid data."""
        updated_user_data = {"first_name": "Jane"}
        updated_user = self.facade.update_user(self.test_user.id, updated_user_data)
        self.assertEqual(updated_user.first_name, "Jane")

    def test_08_update_user_invalid_fields(self):
        """Test updating a user with invalid fields."""
        invalid_user_data = {"email": "invalid-email"} 
        with self.assertRaises(ValueError):
            self.facade.update_user(self.test_user.id, invalid_user_data)

    def test_09_update_user_duplicate_email(self):
        """Test updating a user with an already used email."""
        second_user_data = {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alice@example.com"
        }
        second_user = self.facade.create_user(second_user_data)
        updated_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "alice@example.com"  
        }
        response = self.client.put(f'/api/v1/users/{self.test_user.id}', data=json.dumps(updated_user_data), content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()
