# 🏠 Hbnb - README

## 🌍 Project Overview

Hbnb is a collaborative project developed as part of the second trimester at Holberton School in Cenon, C25 class.
 The goal is to create an Airbnb clone 🏡 to practice real-world software development as if it were a business request in a company. Think of it as training to become the next big startup founder... or at least a bug-fixing master.

## 📁 Project Structure

We choose to follow this structure for our organization :

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

### 📂 Directory & File Descriptions

- **app/**: Main application directory.
  - **api/**: API endpoints (because everyone loves a good REST API, right? 🛠️)
    - **v1/**: Version 1 of the API with resources like users, places, reviews, and amenities.
  - **models/**: Data models for the application (where the magic happens 🧙‍♂️).
  - **services/**: Business logic and service layer.
  - **persistence/**: Handles data storage and retrieval (keeping all the important bits safe 🔒).
- **run.py**: Entry point for running the application 🚀.
- **config.py**: Configuration settings for the project (because chaos is fun, but not in coding 🔧).
- **requirements.txt**: List of dependencies required for the project 📦.
- **README.md**: Documentation for the project (you're reading it right now! 🧐).

## ▶️ Run the Application

To start the application, execute:

```
flask
flask-restx
```
Install the dependencies using:


```
pip install -r requirements.txt
```
Run the application to ensure everything is set up correctly:


```
python run.py
```


## 🔧 Technologies Used

- Language: Python 3 🐍
- Framework: Flask
- API: Flask-RESTx

## 👥 Contributors

- 🦦 Noons-ledev 🦦 : Noah Briet
- 🐦‍⬛ 🌸 Mollydayne 🌸 🐦‍⬛ : Clarisse Perez
- Tom Makni
