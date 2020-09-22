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
    email = forms.EmailField(max_length=254, help_text='Wymagany. Podaj prawidłowy adres e-mail.')
    username = forms.CharField(help_text="Wymagany. Max 150 znaków.")
    password1 = forms.CharField(help_text= "Twoje hasło nie może być zbyt podobne do Twoich innych danych osobowych. Twoje hasło musi zawierać co najmniej 8 znaków. Twoje hasło nie może być hasłem powszechnie używanym. Twoje hasło nie może składać się wyłącznie z liczb.", label="Hasło")
    password2 = forms.CharField(help_text="Hasła muszą być identyczne", label="Powtórz hasło")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BiletyForm(ModelForm):

    class Meta:
        model = Bilety
        fields = ['data', 'ilosc']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['komentarz',]
