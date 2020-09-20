from django.forms import ModelForm
from .models import Kino, DodatkoweInfo
from .models import Ocena, Bilety, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KinoForm(ModelForm):
    class Meta:
        model = Kino
        fields = ['tytul', 'rok', 'opis', 'cena', 'plakat', 'ranking_imdb', 'data']

class DodatkoweInfoForm(ModelForm):
    class Meta:
        model = DodatkoweInfo
        fields = ['czas_trwania', 'gatunek']


class OcenaForm(ModelForm):

    class Meta:
        model = Ocena
        fields = ['recenzja', 'gwiazdki']


class RejestracjaForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'last_name')

class BiletyForm(ModelForm):

    class Meta:
        model = Bilety
        fields = ['data', 'ilosc']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['tytul',]
