from django.urls import path
from .views import film_views, category_views

urlpatterns = [
    path('films/', film_views.get_films, name='film-list'),
    path('films/<int:film_id>/', film_views.get_film, name='get_film'),
    path('films/create/', film_views.create_film, name='create_film'),
    path('films/update/<int:film_id>/', film_views.update_film, name='update_film'),
    path('films/delete/<int:film_id>/', film_views.delete_film, name='delete_film'),
    path('categories/', category_views.get_categories, name='category-list'),
    path('films/<int:film_id>/categories/', category_views.get_categories_of_film, name='get_categories_of_film'),
    path('categories/<int:category_id>/films/', category_views.get_films_of_category, name='category-films'),
]
