from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse
import json
from films.models.Film import Film
from films.models.Category import Category


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