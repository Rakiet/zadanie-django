from rest_framework import serializers


from kinoapp.models import Kino, Bilety, Profile





class BiletySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilety
        fields = ['id', 'ilosc', 'data', 'film']


class KinoSerializer(serializers.ModelSerializer):

    bilet_film = BiletySerializer(many=True, read_only=True)
    class Meta:
        model = Kino
        fields = ['id', 'tytul', 'rok', 'opis', 'cena', 'plakat', 'ranking_imdb', 'bilet_film']


class KinoSerializerMin(serializers.ModelSerializer):

    class Meta:
        model = Kino
        fields = ['id', 'tytul', 'rok']



class BiletySerializerProfilUser(serializers.ModelSerializer):
    film = KinoSerializerMin(many=False)
    class Meta:
        model = Bilety
        fields = ['id', 'ilosc', 'data', 'film']

class ProfileSerializer(serializers.ModelSerializer):
    bilet = BiletySerializerProfilUser()

    class Meta:
        model = Profile
        fields = ['komentarz', 'user', 'bilet']

