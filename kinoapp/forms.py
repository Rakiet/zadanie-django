from django.forms import ModelForm
from .models import Kino, DodatkoweInfo, Ocena

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