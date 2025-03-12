# Task 9 ask us to insert specific data to start with
# Data needed : admin user with a defined id, amenity,

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io',
 '$2b$12$e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', TRUE);

INSERT INTO amenities (id, name) VALUES
(UUID(), 'WiFi'),
(UUID(), 'Swimming Pool'),
(UUID(), 'Air Conditioning');
