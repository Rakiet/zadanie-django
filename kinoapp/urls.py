from django.urls import path
from kinoapp.views import wszystkie_filmy, nowy_film, edytuj_film, usun_film, rejestracja, ocen_film, kup_bilet, potwierdz_zakup


urlpatterns = [
    path('filmy/', wszystkie_filmy, name="wszystkie_filmy"),
    path('nowy/', nowy_film, name="nowy_film"),
    path('edytuj/<int:id>/', edytuj_film, name="edytuj_film"),
    path('usun/<int:id>/', usun_film, name="usun_film"),
    path('rejestracja/', rejestracja, name='rejestracja'),
    path('ocen/<int:id>/', ocen_film, name="ocen_film"),
    path('kup_bilet/<int:id>/', kup_bilet, name="kup_bilet"),
    path('potwierdz_zakup/<int:id>', potwierdz_zakup, name="potwierdz_zakup")
]