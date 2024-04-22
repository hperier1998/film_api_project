# film_api_project
API for the Web Service class at Ynov Aix-en-Provence.

## Project Description
This project is a Django-based WebService allowing the management of a film list.

It provides API endpoints for retrieving, creating, updating, and deleting films (CRUD).

## Installation
Step 1. Clone the repository.
```git clone https://github.com/hperier1998/film_api_project/```

Step 2. Navigate to the project directory. 
```cd film_api_project```

Step 3. Install the dependencies.
```pip install -r requirements.txt```

## Running the API (Django Server)
Step 1. Navigate to the project directory if you're not already there. 

Step 2. Run migrations to create database tables:

```python manage.py makemigrations films```

```python manage.py migrate```


Step 3. Run the Django server.

```python manage.py runserver```

Step 3. The server should now be running at http://localhost:8000/ OR http://127.0.0.1:8000/.

You can access the API endpoints using this base URL.

## Using Postman to interact with the API
Step 1. Open Postman on your computer. ([Download Postman here](https://www.postman.com/downloads/)) <br/>

Step 2. Interact with the API with the following line.
1. **GET** requests.
* Retrieve all the films.

```http://localhost:8000/api/films/``` or ```http://127.0.0.1:8000/api/films/```

* Retrieve a specific film based on it's ID.

```http://localhost:8000/api/films/<film_id>/``` or ```http://127.0.0.1:8000/api/films/<film_id>/```

2. **POST** requests.
* Create a new film.

```http://localhost:8000/api/films/create/``` or ```http://127.0.0.1:8000/api/films/create/```

3. **PUT** requests.
* Update the details of a specific film based on it's ID.

```http://localhost:8000/api/films/update/<film_id>/``` or ```http://127.0.0.1:8000/api/films/update/<film_id>/```


4. **DELETE** requests.
* Delete a specific film.

```http://localhost:8000/api/films/delete/<film_id>/``` or ```http://127.0.0.1:8000/api/films/delete/<film_id>/```


NOTE : Remember to set the appropriate request type (GET, POST, PUT, DELETE) and URL in Postman. 

For POST and PUT requests, include the required parameters in the request body in the JSON format shown below.
```
{
    "name": "tata",
    "description": "tata est bien",
    "publication_date": "2024-04-22",
    "note": 3
}
```
