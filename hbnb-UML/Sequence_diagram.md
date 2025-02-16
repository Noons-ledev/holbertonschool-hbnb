First here we have a sequence for a User registration case : 
 ```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Persistence

    User->>API: Send registration data (name, email, password)
    API->>BusinessLogic: Validate input data (email, password)

    alt Valid input
        BusinessLogic->>BusinessLogic: Hash password (if needed)
        BusinessLogic->>Persistence: Save user data to database
        Persistence->>BusinessLogic: Confirm user saved
        BusinessLogic->>API: Return success
        API->>User: HTTP 201 - User created successfully
        
    else Database error (HTTP 500)
        Persistence->>API: Return error (HTTP 500 - Database failure)
        API->>User: HTTP 500 - Internal Server Error
       
    else Invalid input (missing password or existing email)
        BusinessLogic->>BusinessLogic: Detects Invalid input
        BusinessLogic->>API: Return error (password required)
        API->>User: HTTP 400 + Error message
    end
```

It show how the app will interact in a case where a user is trying to create an account

The following case is about Place creation : 

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogicLayer
    participant PersistenceLayer

    User->>API: POST /places (title, description, price, lat, long, photos, amenities)
    API->>BusinessLogicLayer: validateRequest (data)
    BusinessLogicLayer->>PersistenceLayer: createPlace (data)
        alt Insert Success
            PersistenceLayer-->>BusinessLogicLayer: return new Place (id)
            BusinessLogicLayer-->>API: return Response (201, place)
            API-->>User: Response (201 Created) JSON (place)

        else Missing required fields (photos, amenities, etc.)
        BusinessLogicLayer ->> BusinessLogicLayer: Detects invalid input
        BusinessLogicLayer-->>API: return Response (400, "Missing required fields")
        API-->>User: Response (400 Bad Request) JSON (error)
     

        else Insert Failed
            PersistenceLayer-->>BusinessLogicLayer: return Response (500, "Database Error")
            BusinessLogicLayer-->>API: return Response (500, "Database Error")
            API-->>User: Response (500 Internal Server Error) JSON (error)
        end
```
Next Diagram is about the Review Submission : A user tries to submit a review to a place

```mermaid

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    %% Soumission d'une nouvelle review
    User ->> API: POST /reviews (rating, comment, place_id)
    API ->> BusinessLogic: Validate input
    alt Valid Data
     BusinessLogic ->> Database: Check if user exists
        Database -->> BusinessLogic: User verified
        BusinessLogic ->> Database: Insert review (user_id, place_id, rating, comment)
        Database -->> BusinessLogic: Review saved
        BusinessLogic -->> API: Return success (201 Created)
        API -->> User: 201 Created (Review submitted)
    else Invalid Data
        BusinessLogic -->> API: Return error (400 Bad Request)
        API -->> User: 400 Bad Request (Invalid review data)
    else Database error
        Database -->> BusinessLogic: Error Occurs
        BusinessLogic -->> API: Return HTTP 500 Status code
        API -->> User: HTTP 500 Internal Server Error
        
    end
    %% Récupération d'une review existante
    User ->> API: GET /reviews/{review_id}
    API ->> BusinessLogic: Fetch review
    BusinessLogic ->> Database: Get review by ID
    Database -->> BusinessLogic: Return review details
    BusinessLogic -->> API: Send review details
    API -->> User: 200 OK (Review data)
    alt Review Not Found
        Database -->> BusinessLogic: Review does not exist
        BusinessLogic -->> API: Return error (404 Not Found)
        API -->> User: 404 Not Found (Review does not exist)
    end
```

In the next case, the User is trying to fetch a list of places :

```mermaid
sequenceDiagram
    User ->> API: HTTP Request "GET" to fetch a list of places
    API ->> BusinessLogic: Recieving request,processing it, and calling BusinessLogic
    alt Valid Input
    BusinessLogic ->> Database:performs any validation or additional processing if needed then queries Persistence for data
    Database ->> BusinessLogic: Retrieves the list of corresponding places
    BusinessLogic ->> API: processes the data and returns it to the API
    API ->> User: Returns 200 HTTP status code and a list of places(empty if no one is matching)
    else Missing parameters (check_in_date, check_out_date, location)
    BusinessLogic ->> BusinessLogic: Detects invalid input and raises an exception
    BusinessLogic ->> API: Send the raised exception
    API ->> User: Returns HTTP 400 and an error message
    else Database Error
    BusinessLogic ->> Database: Queries Database
    Database ->> Database: Error Occurs
    Database ->> BusinessLogic: Query fails (DB ISSUE). Error message or error object
    BusinessLogic ->> API: Return HTTP 500 status code
    API --> User : Return HTTP 500 with Internal Server Error message
    end
```
