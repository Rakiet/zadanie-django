from django.urls import path
from kinoapp.views import wszystkie_filmy, nowy_film, edytuj_film, usun_film, rejestracja


urlpatterns = [
    path('filmy/', wszystkie_filmy, name="wszystkie_filmy"),
    path('nowy/', nowy_film, name="nowy_film"),
    path('edytuj/<int:id>/', edytuj_film, name="edytuj_film"),
    path('usun/<int:id>/', usun_film, name="usun_film"),
    path('rejestracja/', rejestracja, name='rejestracja'),
]