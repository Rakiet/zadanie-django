from django.urls import path
from kinoapp.views import wszystkie_filmy, nowy_film, edytuj_film


urlpatterns = [
    path('filmy/', wszystkie_filmy),
    path('nowy/', nowy_film),
    path('edytuj/<int:id>/', edytuj_film),
]