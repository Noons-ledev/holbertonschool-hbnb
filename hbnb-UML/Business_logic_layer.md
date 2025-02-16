The ClassDiagram of our HBNB project : 
 ```mermaid
classDiagram
  class BaseModel {
    <<abstract>>
    +UUID id
    +DATE created_at
    +DATE updated_at
    +delete()
    +update()
  }

  class User {
    +string first_name
    +string last_name
    -string email
    -string password
    +boolean is_admin
    +set_password(password)
    +check_password(password)
    +sign_up()
    +login()
    +write_review()
    +delete()
    +update()
  }

  class Place {
    +string name
    +string location
    +float average_rating
    +float price
    +string currency
    -UUID owner_id
    +get_owner()
    +add_amenity()
    +remove_amenity()
    +delete()
    +update()
  }

  class Review {
    -UUID user_id
    -UUID place_id
    +int rating
    +string comment
    +write_review()
    +get_user()
    +get_place()
    +delete()
    +update()
  }

  class Amenity {
    +UUID id
    +string name
    +display(place_id)
    +delete()
    +update()
  }

  class AmenityPlace {
    -UUID amenity_id
    -UUID place_id
  }

BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Amenity
BaseModel <|-- Review

Place "1" --> "0..n" AmenityPlace
Amenity "1" --> "0..n" AmenityPlace
User "1" --> "0..n" Review : Writes
User "1" *-- "0..n" Place : Owns
Place "1" *-- "0..n" Review : Has
```
