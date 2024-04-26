# film_api_project
API for the Web Service class at Ynov Aix-en-Provence.

## Project Description
This project is a Django-based WebService allowing the management of a film list.

It provides API endpoints for retrieving, creating, updating, and deleting films (CRUD).

## Table of contents
- [Installation](#Installation)
- [Running the API](#Running the API)
- [Using Postman to interact with the API](#Using Postman to interact with the API)

## Installation
Step 1. Clone the repository.
```git clone https://github.com/hperier1998/film_api_project/```

Step 2. Navigate to the project directory. 
```cd film_api_project```

Step 3. Install the dependencies.
```pip install -r requirements.txt```

## Running the API
Step 1. Navigate to the project directory if you're not already there. 

Step 2. Run migrations to create database tables:

```python manage.py makemigrations films```

```python manage.py migrate```


Step 3. Run the Django server.

```python manage.py runserver```

Step 3. The server should now be running at http://localhost:8000/ OR http://127.0.0.1:8000/.

You can access the API endpoints using this base URL.

## Using Postman to interact with the API
Step 1. Open Postman on your computer. ([Download Postman here](https://www.postman.com/downloads/))

Step 2. You can now start interacting with the API by using the following URLs.

Remember to set the correct **METHOD** in Postman.

### GET Requests
For all of the GET requests, the data can be retrieved in XML format by adding the header 'Accept' with the value 'application/xml' in Postman.

![Screenshot of where to define the header in Postman to retrieve the data in XML format](/assets/images/xml_header_instruction.png)

#### 1. Retrieve all films
```
http://localhost:8000/api/films/
http://127.0.0.1:8000/api/films/
```

#### 2. Retrieve films by page
```
http://localhost:8000/api/films/?page=<page_number>
http://127.0.0.1:8000/api/films/?page=<page_number>
```

Replace <page_number> with the page number.

#### 3. Retrieve a specific film based on it's ID
```
http://localhost:8000/api/films/<film_id>/
http://127.0.0.1:8000/api/films/<film_id>/
```

Replace <film_id> with the id of the film.

#### 4. Retrieve films by title
```
http://localhost:8000/api/films/?title=<title>
http://127.0.0.1:8000/api/films/?title=<title>
```

Replace <title> with the title of the film.

#### 5. Retrieve films by description
```
http://localhost:8000/api/films/?description=<description>
http://127.0.0.1:8000/api/films/?description=<description>
```

Replace <description> with a word (or more) of the description of the film.

#### 6. Retrieve films by title and description
```
http://localhost:8000/api/films/?title=<title>&description=<description>
http://127.0.0.1:8000/api/films/?title=<title>&description=<description>
```

Replace <title> with the title of the film and <description> with a word (or more) of the description of the film.

#### 7. Retrieve all categories
```
http://localhost:8000/api/categories/
http://127.0.0.1:8000/api/categories/
```

#### 8. Retrieve the categories of a specific film based on it's ID
```
http://localhost:8000/api/films/<film_id>/categories/
http://127.0.0.1:8000/api/films/<film_id>/categories/
```

Replace <film_id> with the id of the film.

#### 9. Retrieve films by category
```
http://localhost:8000/api/categories/<category_id>/films/
http://127.0.0.1:8000/api/categories/<category_id>/films/
```

Replace <category_id> with the id of the category.

### POST Requests

#### 1. Create a new film
```
http://localhost:8000/api/films/create/
http://127.0.0.1:8000/api/films/create/
```

Example of the JSON format to create a new film.

```
{
    "name": "New Film",
    "description": "Description of New Film",
    "publication_date": "2024-04-23",
    "note": 4,
    "categories": [1, 2, 3]
}
```

### PUT Requests

#### 1. Update the details of a specific film based on it's ID
```
http://localhost:8000/api/films/update/<film_id>/
http://127.0.0.1:8000/api/films/update/<film_id>/
```

Replace <film_id> with the id of the film to update.

Example of the JSON format to update an existing film.

```
{
    "name": "Modified title",
    "description": "Modified description",
    "publication_date": "2024-04-23",
    "note": 2,
    "categories": [5]
}
```

NOTE : You are not required to put all the values, you can also just put the value to modify.

```
{
    "categories": [1]
}
```

### DELETE Requests

#### 1. Delete a specific film
```
http://localhost:8000/api/films/delete/<film_id>/
http://127.0.0.1:8000/api/films/delete/<film_id>/
```

Replace <film_id> with the id of the film to delete.