from rest_framework import serializers
from kinoapp.models import Kino, Bilety, Profile
from django.contrib.auth.models import User





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
        fields = ['id','komentarz', 'user', 'bilet']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'])
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'komentarz', 'user', 'bilet']

