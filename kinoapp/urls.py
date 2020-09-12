from django.urls import path
from kinoapp.views import wszystkie_filmy


urlpatterns = [
    path('filmy/', wszystkie_filmy)
]