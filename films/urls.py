from django.urls import path
from . import views


urlpatterns = [
    # path('films/', views.get_films, name='get_films'),
    path('films/', views.get_films, name='film-list'),
    path('films/<int:film_id>/', views.get_film, name='get_film'),
    path('films/create/', views.create_film, name='create_film'),
    path('films/update/<int:film_id>/', views.update_film, name='update_film'),
    path('films/delete/<int:film_id>/', views.delete_film, name='delete_film'),
]
