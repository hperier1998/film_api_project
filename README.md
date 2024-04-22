# film_api_project
API for the Web Service class at Ynov Aix-en-Provence.

## Project Description
This project is a Django-based WebService allowing the management of a film list.
It provides API endpoints for retrieving, creating, updating, and deleting films (CRUD).

## Installation
Step 1. Clone the repository. <br/>
```git clone https://github.com/hperier1998/film_api_project/```

Step 2. Navigate to the project directory. <br/>
```cd film_api_project```

Step 3. Install the dependencies. <br/>
```pip install -r requirements.txt```

## Running the API (Django Server)
Step 1. Navigate to the project directory if you're not already there. <br/>

Step 2. Run the Django server. <br/>
```python manage.py runserver```

Step 3. The server should now be running at http://localhost:8000/. 
You can access the API endpoints using this base URL.

## Using Postman to interact with the API
Step 1. Open Postman on your computer. <br/>

Step 2. Interact with the API with the following line. <br/>
1. GET requests.
* Retrieve all the films.
```http://localhost:8000/api/films/```
* Retrieve a specific film based on it's ID.
```http://localhost:8000/api/films/<film_id>/```

2. POST requests.
* Create a new film.
```http://localhost:8000/api/films/create/```

3. PUT requests.
* Update the details of a specific film based on it's ID.
```http://localhost:8000/api/films/update/<film_id>/```

4. DELETE requests.
* Delete a specific film.
```http://localhost:8000/api/films/delete/<film_id>/```

NOTE : Remember to set the appropriate request type (GET, POST, PUT, DELETE) and URL in Postman. <br/>
For POST and PUT requests, include the required parameters in the request body in JSON format.