import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db  # Importer l'application Flask
from app.models import Place, User, Review, Amenity

class TestPlaceModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Crée l'application Flask et initialise un contexte."""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()  # Active le contexte de l'application

    @classmethod
    def tearDownClass(cls):
        """Supprime le contexte de l'application après les tests."""
        cls.app_context.pop()

    def setUp(self):
        """Utilise la base de données réelle et une session active."""
        self.session = db.session

        # Création d'un utilisateur propriétaire du lieu
        self.owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        self.session.add(self.owner)
        self.session.commit()

    def tearDown(self):
        """Nettoyage après chaque test (optionnel)."""
        self.session.rollback()  # Annule les transactions non validées

        # Nettoie toutes les tables après chaque test (optionnel, à commenter si tu veux garder les tests)
        for table in reversed(db.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_place_creation(self):
        """Test la création d'un lieu avec un propriétaire."""
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=self.owner
        )
        self.session.add(place)
        self.session.commit()

        retrieved_place = self.session.query(Place).filter(Place.title == "Cozy Apartment").first()
        self.assertIsNotNone(retrieved_place, "Le lieu n'a pas été inséré en base de données.")
        self.assertEqual(retrieved_place.price, 100)
        self.assertEqual(retrieved_place.owner.email, "alice.smith@example.com")

    def test_place_add_review(self):
        """Test l'ajout et la récupération d'une review associée à un lieu."""
        place = Place(
            title="Mountain Cabin",
            description="A peaceful retreat in the mountains",
            price=120,
            latitude=35.6895,
            longitude=139.6917,
            owner=self.owner
        )
        self.session.add(place)
        self.session.commit()

        review = Review(text="Incredible stay!", rating=5, place=place, user=self.owner)
        self.session.add(review)
        self.session.commit()

        retrieved_place = self.session.query(Place).filter(Place.title == "Mountain Cabin").first()
        self.assertIsNotNone(retrieved_place, "Le lieu n'a pas été inséré en base de données.")
        self.assertEqual(len(retrieved_place.reviews), 1)
        self.assertEqual(retrieved_place.reviews[0].text, "Incredible stay!")

    def test_place_add_amenity(self):
        """Test l'ajout d'une amenity à un lieu."""
        place = Place(
            title="Luxury Penthouse",
            description="An ultra-modern penthouse",
            price=500,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.owner
        )
        self.session.add(place)
        self.session.commit()

        amenity = Amenity(name="Swimming Pool")
        self.session.add(amenity)
        self.session.commit()

        place.amenities.append(amenity)
        self.session.commit()

        retrieved_place = self.session.query(Place).filter(Place.title == "Luxury Penthouse").first()
        self.assertIsNotNone(retrieved_place, "Le lieu n'a pas été inséré en base de données.")
        self.assertEqual(len(retrieved_place.amenities), 1)
        self.assertEqual(retrieved_place.amenities[0].name, "Swimming Pool")

    def test_place_price_validation(self):
        """Test que le prix ne peut pas être négatif."""
        with self.assertRaises(ValueError) as context:
            place = Place(
                title="Negative Price House",
                description="This should not be allowed",
                price=-10,  # Prix négatif
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.owner
            )
            self.session.add(place)
            self.session.commit()
        self.assertEqual(str(context.exception), "Price must be positive.")

    def test_place_invalid_coordinates(self):
        """Test que les coordonnées sont valides."""
        with self.assertRaises(ValueError) as context:
            place = Place(
                title="Invalid Latitude",
                description="This should not be allowed",
                price=50,
                latitude=100.00,  # Latitude invalide (> 90)
                longitude=-74.0060,
                owner=self.owner
            )
            self.session.add(place)
            self.session.commit()
        self.assertEqual(str(context.exception), "latitude must be between -90 and 90.")

        with self.assertRaises(ValueError) as context:
            place = Place(
                title="Invalid Longitude",
                description="This should not be allowed",
                price=50,
                latitude=40.7128,
                longitude=-200,  # Longitude invalide (< -180)
                owner=self.owner
            )
            self.session.add(place)
            self.session.commit()

    def test_place_update(self):
        """Test la mise à jour des informations d'un lieu."""
        place = Place(
            title="Old House",
            description="Needs some renovations",
            price=80,
            latitude=35.6895,
            longitude=139.6917,
            owner=self.owner
        )
        self.session.add(place)
        self.session.commit()

        place.title = "Renovated House"
        place.price = 120
        self.session.commit()

        retrieved_place = self.session.query(Place).filter(Place.title == "Renovated House").first()
        self.assertIsNotNone(retrieved_place, "Le lieu mis à jour n'a pas été trouvé en base de données.")
        self.assertEqual(retrieved_place.price, 120)

    def test_place_deletion(self):
        """Test la suppression d'un lieu et la suppression en cascade des reviews et amenities."""
        place = Place(
            title="Test Place",
            description="Just a test place",
            price=60,
            latitude=51.5074,
            longitude=-0.1278,
            owner=self.owner
        )
        self.session.add(place)
        self.session.commit()

        review = Review(text="Not bad!", rating=4, place=place, user=self.owner)
        amenity = Amenity(name="WiFi")
        self.session.add(review)
        self.session.add(amenity)
        self.session.commit()

        place.reviews.append(review)
        place.amenities.append(amenity)
        self.session.commit()

        self.session.delete(place)
        self.session.commit()

        deleted_place = self.session.query(Place).filter_by(title="Test Place").first()
        remaining_reviews = self.session.query(Review).filter_by(place_id=place.id).all()
        remaining_amenities = self.session.query(Amenity).filter(Amenity.places.any(id=place.id)).all()

        self.assertIsNone(deleted_place, "Le lieu n'a pas été supprimé.")
        self.assertEqual(len(remaining_reviews), 0, "Les reviews associées n'ont pas été supprimées.")
        self.assertEqual(len(remaining_amenities), 0, "Les amenities associées n'ont pas été supprimées.")

if __name__ == "__main__":
    unittest.main()
