import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.basemodel import BaseModel
from app.test_alex.test_database import setup_in_memory_db


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """Initialise une nouvelle base de données en mémoire pour chaque test."""
        self.Session, self.engine = setup_in_memory_db()
        self.session = self.Session()

    def tearDown(self):
        """Ferme la session et détruit la base après chaque test."""
        self.session.close()
        self.engine.dispose()

    def test_user_creation(self):
        """Test la création d'un utilisateur avec hachage du mot de passe."""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.session.add(user)
        self.session.commit()

        retrieved_user = self.session.query(User).filter_by(email="john.doe@example.com").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, "John")
        self.assertEqual(retrieved_user.last_name, "Doe")
        self.assertEqual(retrieved_user.email, "john.doe@example.com")
        self.assertFalse(retrieved_user.is_admin)

    def test_user_max_length(self):
        """Test les limites de longueur des noms."""
        
        with self.assertRaises(ValueError) as context:
            user = User(first_name="A" * 51, last_name="Doe", email="john.doe@example.com")
            self.session.add(user)
            self.session.commit()
        self.assertEqual(str(context.exception), "First name must be at most 50 characters")

        with self.assertRaises(ValueError) as context:
            user = User(first_name="John", last_name="B" * 51, email="john.doe@example.com")
            self.session.add(user)
            self.session.commit()
        self.assertEqual(str(context.exception), "Last name must be at most 50 characters")

    def test_user_email(self):
        """Test les formats d'email invalides."""
        with self.assertRaises(ValueError) as context:
            user = User(first_name="John", last_name="Doe", email="john.doeexample.com")
            self.session.add(user)
            self.session.commit()
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_user_required_fields(self):
        """Test les champs obligatoires."""

        with self.assertRaises(IntegrityError):
            user = User(first_name="John", last_name="Doe")
            self.session.add(user)
            self.session.commit()
        self.session.rollback()

        with self.assertRaises(IntegrityError):
            user = User(first_name="John", email="john.doe@example.com")
            self.session.add(user)
            self.session.commit()
        self.session.rollback()

        with self.assertRaises(IntegrityError):
            user = User(last_name="Doe", email="john.doe@example.com")
            self.session.add(user)
            self.session.commit()
        self.session.rollback()

if __name__ == "__main__":
    unittest.main()
