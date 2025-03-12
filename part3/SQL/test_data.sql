# Molly : not needed by task 9, but I think it might b usefull to have test data
# Data test possible : users (us!), places


INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
(UUID(), 'Molly', 'Dayne', 'molly@example.com', 'hashed_password', FALSE),
(UUID(), 'Noons', 'Ledev', 'noons@example.com', 'hashed_password', FALSE);

