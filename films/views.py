from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Film
import json


@csrf_exempt
def get_films(request):
    """
    Retrieve paginated details of all films, with optional search by title or description.
    """
    # Retrieve all films
    films = Film.objects.all()

    # Handle search query parameters
    title_query = request.GET.get('title')
    description_query = request.GET.get('description')

    if title_query:
        films = films.filter(name__icontains=title_query)

    if description_query:
        films = films.filter(description__icontains=description_query)

    # Pagination
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    paginator = Paginator(films, page_size)
    paginated_films = paginator.get_page(page_number)

    # Check the Accept header to determine the response format
    accept_header = request.headers.get('Accept', '')

    if 'application/xml' in accept_header:
        # Serialize data to XML
        films_xml = serialize('xml', paginated_films)
        return HttpResponse(films_xml, content_type='application/xml', status=200)
    else:
        # Serialize data to JSON
        films_data = []
        for film in paginated_films:
            categories = [category.name for category in film.categories.all()]  # Get categories associated with the film
            films_data.append({
                "id": film.id,
                "name": film.name,
                "description": film.description,
                "publication_date": film.publication_date.strftime("%Y-%m-%d"),
                "note": film.note,
                "categories": categories
            })

        # Pagination links
        next_page_url = reverse('film-list') + f"?page={paginated_films.next_page_number()}" if paginated_films.has_next() else None
        prev_page_url = reverse('film-list') + f"?page={paginated_films.previous_page_number()}" if paginated_films.has_previous() else None

        return JsonResponse({
            "results": films_data,
            "pagination": {
                "page": paginated_films.number,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "next_page": next_page_url,
                "prev_page": prev_page_url
            }
        }, status=200)


@csrf_exempt
def get_film(request, film_id):
    """
    Retrieve details of a specific film.
    """
    try:
        film = Film.objects.get(id=film_id)

        # Check the Accept header to determine the response format
        accept_header = request.headers.get('Accept', '')

        if 'application/xml' in accept_header:
            # Serialize data to XML
            film_xml = serialize('xml', [film])
            return HttpResponse(film_xml, content_type='application/xml', status=200)
        else:
            # Serialize film data to JSON
            film_data = {
                "id": film.id,
                "name": film.name,
                "description": film.description,
                "publication_date": film.publication_date.strftime("%Y-%m-%d"),
                "note": film.note
            }

            return JsonResponse(film_data, status=200)
    except Film.DoesNotExist:
        return JsonResponse({"error": "Film not found"}, status=404)


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
