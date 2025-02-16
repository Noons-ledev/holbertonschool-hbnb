Here is our High level package diagram of the hbnb project


```mermaid
graph TB
    A[**Presentation**
        UserAPI
        PlacesAPI
        ReviewsAPI
        AmenitiesAPI]
    
    B[**Business Logic**
     User Model
     Places Model
     Reviews Model
     Amenitites Model]
    
    C[**Persistence**
    Database Access]

    A-->|Facade Interface|B 
    B-->|Database operations|C
