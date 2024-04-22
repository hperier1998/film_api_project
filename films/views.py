from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Film
import json


@csrf_exempt
def get_films(request):
    """
    Retrieve details of all films.
    """
    films = Film.objects.all()
    films_data = [{"id": film.id, "name": film.name, "description": film.description,
                   "publication_date": film.publication_date.strftime("%Y-%m-%d"), "note": film.note} for film in films]

    return JsonResponse(films_data, safe=False, status=200)


@csrf_exempt
def get_film(request, film_id):
    """
    Retrieve details of a specific film.
    """
    try:
        film = Film.objects.get(id=film_id)
        film_data = {"id": film.id, "name": film.name, "description": film.description,
                     "publication_date": film.publication_date.strftime("%Y-%m-%d"), "note": film.note}

        return JsonResponse(film_data, status=200)

    except Film.DoesNotExist:
        return HttpResponseNotFound("Film not found", status=404)


@csrf_exempt
def create_film(request):
    """
    Create a new film.
    """
    if request.method == 'POST':
        try:
            # Extract film data from request
            data = json.loads(request.body)

            # Create a new film instance
            film = Film.objects.create(
                name=data['name'],
                description=data['description'],
                publication_date=data['publication_date'],
                note=data.get('note', None)
            )

            return JsonResponse({"message": "Film created"}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data", status=400)
    else:
        return HttpResponseBadRequest("Method not allowed", status=400)


@csrf_exempt
def update_film(request, film_id):
    """
    Update the details of a specific film.
    """
    if request.method == 'PUT':
        try:
            # Extract updated film data from request
            data = json.loads(request.body)

            # Retrieve the film to update
            try:
                film = Film.objects.get(id=film_id)
            except Film.DoesNotExist:
                return HttpResponseNotFound("Film not found")

            # Update film fields
            film.name = data.get('name', film.name)
            film.description = data.get('description', film.description)
            film.publication_date = data.get('publication_date', film.publication_date)
            film.note = data.get('note', film.note)

            # Save the updated film
            film.save()

            return JsonResponse({"message": "Film updated"}, status=200)

        except Film.DoesNotExist:
            return HttpResponseNotFound("Film not found", status=404)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data", status=400)

    else:
        return HttpResponseBadRequest("Method not allowed", status=400)



@csrf_exempt
def delete_film(request, film_id):
    """
    Delete a specific film.
    """
    if request.method == 'DELETE':
        try:
            # Retrieve the film to delete
            film = Film.objects.get(id=film_id)

            # Delete the film
            film.delete()

            return JsonResponse({"message": "Film deleted"}, status=200)

        except Film.DoesNotExist:
            return HttpResponseNotFound("Film not found", status=404)

        except Film.DoesNotExist:
            return HttpResponseNotFound("Film not found", status=400)

    else:
        return HttpResponseBadRequest("Method not allowed", status=400)
