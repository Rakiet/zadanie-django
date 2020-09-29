from rest_framework import serializers
from kinoapp.models import Kino

class KinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = ['tytul', 'rok', 'opis', 'cena', 'plakat', 'ranking_imdb', 'data']