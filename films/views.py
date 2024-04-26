from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Film, Category
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
            # Construct hypermedia links
            film_link = reverse('get_film', kwargs={'film_id': film.id})
            categories_link = reverse('get_categories_of_film', kwargs={'film_id': film.id})

            films_data.append({
                "id": film.id,
                "name": film.name,
                "description": film.description,
                "publication_date": film.publication_date.strftime("%Y-%m-%d"),
                "note": film.note,
                "categories":  [{"id": category.id, "name": category.name} for category in film.categories.all()],
                "links": {
                    "film_link": {"href": film_link},
                    "categories_link": {"href": categories_link}
                }
            })

        # Construct hypermedia links
        film_list_link = reverse('film-list')

        # Include title filter in self_link if present
        if title_query:
            film_list_link += f"?title={title_query}"

        # Include description filter in self_link if present
        if description_query:
            # If title_query is present, add '&' else add '?'
            separator = '&' if title_query else '?'
            film_list_link += f"{separator}description={description_query}"

        # Pagination links
        separator = '&' if title_query or description_query else '?'
        self_link = film_list_link + f"{separator}page={paginated_films.number}"
        next_page_url = film_list_link + f"{separator}page={paginated_films.next_page_number()}" if paginated_films.has_next() else None
        prev_page_url = film_list_link + f"{separator}page={paginated_films.previous_page_number()}" if paginated_films.has_previous() else None

        return JsonResponse({
            "results": films_data,
            "pagination": {
                "page": paginated_films.number,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "next_page": next_page_url,
                "prev_page": prev_page_url,
                "current_page": self_link
            }
        }, safe=False, status=200)


@csrf_exempt
def get_film(request, film_id):
    """
    Retrieve details of a specific film.
    """
    try:
        film = Film.objects.get(id=film_id)

        # Construct hypermedia links
        self_link = reverse('get_film', kwargs={'film_id': film_id})
        categories_link = reverse('get_categories_of_film', kwargs={'film_id': film_id})

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
                "note": film.note,
                "categories": [{"id": category.id, "name": category.name} for category in film.categories.all()],
                "links": {
                    "categories_link": {"href": categories_link}
                },
                "pagination": {
                    "current_page": self_link,
                }
            }

            return JsonResponse(film_data, safe=False, status=200)
    except Film.DoesNotExist:
        return JsonResponse({"error": "Film not found"}, status=404)


@csrf_exempt
def get_categories(request):
    """
    Retrieve paginated details of all categories.
    """
    categories = Category.objects.all()

    # Check the Accept header to determine the response format
    accept_header = request.headers.get('Accept', '')

    if 'application/xml' in accept_header:
        # Serialize data to XML
        categories_xml = serialize('xml', categories)
        return HttpResponse(categories_xml, content_type='application/xml', status=200)
    else:
        # Serialize data to JSON
        category_data = [{"id": category.id, "name": category.name} for category in categories]

        # Construct hypermedia links
        self_link = reverse('category-list')

        return JsonResponse({
            "results": category_data,
            "pagination": {
                "current_page": self_link,
            }
        }, safe=False, status=200)


@csrf_exempt
def get_categories_of_film(request, film_id):
    """
    Retrieve categories of a specific film.
    """
    try:
        film = Film.objects.get(id=film_id)
        categories = film.categories.all()

        # Construct hypermedia links
        self_link = reverse('get_categories_of_film', kwargs={'film_id': film_id})

        # Check the Accept header to determine the response format
        accept_header = request.headers.get('Accept', '')

        if 'application/xml' in accept_header:
            # Serialize data to XML
            categories_xml = serialize('xml', categories)
            return HttpResponse(categories_xml, content_type='application/xml', status=200)
        else:
            categories_data = [{"id": category.id, "name": category.name}
                               for category in categories]

            # Construct HAL response
            response_data = {
                "categories": categories_data,
                "links": {
                    "film": {"href": reverse('get_film', kwargs={'film_id': film_id})},
                },
                "pagination": {
                    "current_page": self_link,
                }
            }

            return JsonResponse(response_data, safe=False, status=200)
    except Film.DoesNotExist:
        return JsonResponse({"error": "Film not found"}, status=404)


@csrf_exempt
def get_films_of_category(request, category_id):
    """
    Retrieve films belonging to a specific category.
    """
    try:
        # Retrieve the category object
        category = Category.objects.get(id=category_id)

        # Get the films associated with the category
        films = category.film_set.all()

        # Pagination
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        paginator = Paginator(films, page_size)
        paginated_films = paginator.get_page(page_number)

        # Check the Accept header to determine the response format
        accept_header = request.headers.get('Accept', '')

        if 'application/xml' in accept_header:
            # Serialize films data to XML
            films_xml = serialize('xml', films)
            return HttpResponse(films_xml, content_type='application/xml', status=200)
        else:
            # Serialize data to JSON
            films_data = []
            for film in paginated_films:
                # Construct hypermedia links
                film_link = reverse('get_film', kwargs={'film_id': film.id})
                categories_link = reverse('get_categories_of_film', kwargs={'film_id': film.id})

                films_data.append({
                    "id": film.id,
                    "name": film.name,
                    "description": film.description,
                    "publication_date": film.publication_date.strftime("%Y-%m-%d"),
                    "note": film.note,
                    "categories": [{"id": category.id, "name": category.name} for category in film.categories.all()],
                    "links": {
                        "film_link": {"href": film_link},
                        "categories_link": {"href": categories_link}
                    }
                })

            # Construct hypermedia links
            self_link = reverse('category-films', args=[category_id]) + f"?page={paginated_films.number}"

            # Pagination links
            next_page_url = reverse('category-films', args=[category_id]) + f"?page={paginated_films.next_page_number()}" if paginated_films.has_next() else None
            prev_page_url = reverse('category-films', args=[category_id]) + f"?page={paginated_films.previous_page_number()}" if paginated_films.has_previous() else None

            return JsonResponse({
                "results": films_data,
                "pagination": {
                    "page": paginated_films.number,
                    "total_pages": paginator.num_pages,
                    "total_results": paginator.count,
                    "next_page": next_page_url,
                    "prev_page": prev_page_url,
                    "current_page": self_link,
                }
            }, safe=False, status=200)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)


@csrf_exempt
def create_film(request):
    """
    Create a new film.
    """
    if request.method == 'POST':
        try:
            # Extract film data from request
            data = json.loads(request.body)

            # Check if categories are provided
            if 'categories' not in data or not data['categories']:
                return JsonResponse({"error": "Categories are required"}, status=400)

            # Create a new film instance
            film = Film.objects.create(
                name=data['name'],
                description=data['description'],
                publication_date=data['publication_date'],
                note=data.get('note', None)
            )

            # Add categories to the film
            categories_ids = data.get('categories', [])
            for category_id in categories_ids:
                try:
                    category = Category.objects.get(id=category_id)
                    film.categories.add(category)
                except Category.DoesNotExist:
                    return JsonResponse({"error": "Category not found"}, status=404)

            return JsonResponse({
                "message": "Film created",
                "links": {
                    "film": {"href": reverse('get_film', kwargs={'film_id': film.id})}
                }
            }, status=201)
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

            # Update categories
            categories_ids = data.get('categories', [])
            film.categories.clear()
            for category_id in categories_ids:
                try:
                    category = Category.objects.get(id=category_id)
                    film.categories.add(category)
                except Category.DoesNotExist:
                    return JsonResponse({"error": "Category not found"}, status=404)

            return JsonResponse({
                "message": "Film updated",
                "links": {
                    "film": {"href": reverse('get_film', kwargs={'film_id': film.id})}
                }
            }, status=200)

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
