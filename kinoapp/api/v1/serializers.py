from rest_framework import serializers
from kinoapp.models import Kino, Bilety





class BiletySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilety
        fields = ['id', 'ilosc', 'data']


class KinoSerializer(serializers.ModelSerializer):

    bilet = BiletySerializer(many=True, read_only=True)
    class Meta:
        model = Kino
        fields = ['id', 'tytul', 'rok', 'opis', 'cena', 'plakat', 'ranking_imdb', 'bilet']