from django.urls import path
from kinoapp.views import wszystkie_filmy, nowy_film


urlpatterns = [
    path('filmy/', wszystkie_filmy),
    path('nowy/', nowy_film)
]