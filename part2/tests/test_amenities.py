import unittest
import uuid
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository
from app import create_app
from flask import json

import unittest
import uuid
from app import create_app
from flask import json

class TestAmenityAPI(unittest.TestCase):
    """Test cases for the Amenity API."""

    def setUp(self):
        """Setup test client and sample data."""
        self.app = create_app().test_client()
        self.amenity_data = {"name": "Pool"}

        response = self.app.post("/api/v1/amenities/", data=json.dumps(self.amenity_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.amenity = response.json
    
    def test_create_amenity_success(self):
        """Test successful amenity creation."""
        new_amenity = {"name": "Gym"}
        response = self.app.post("/api/v1/amenities/", data=json.dumps(new_amenity), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], new_amenity["name"])
    
    def test_get_amenity_success(self):
        """Test retrieving an amenity by ID."""
        response = self.app.get(f"/api/v1/amenities/{self.amenity['id']}")
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity."""
        non_existent_id = str(uuid.uuid4())
        response = self.app.get(f"/api/v1/amenities/{non_existent_id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_amenities(self):
        """Test retrieving all amenities."""
        response = self.app.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
    
    def test_update_amenity_success(self):
        """Test updating an amenity with valid data."""
        updated_data = {"name": "Updated Pool"}
        response = self.app.put(
            f"/api/v1/amenities/{self.amenity['id']}",
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_empty_name(self):
        """Test attempting to update an amenity with an empty name."""
        response = self.app.put(
            f"/api/v1/amenities/{self.amenity['id']}",
            data=json.dumps({"name": ""}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_not_found(self):
        """Test attempting to update a non-existent amenity."""
        non_existent_id = str(uuid.uuid4())
        updated_data = {"name": "NonExistentAmenity"}
        response = self.app.put(
            f"/api/v1/amenities/{non_existent_id}",
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

