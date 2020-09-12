from django.forms import ModelForm
from .models import Kino

class KinoForm(ModelForm):
    class Meta:
        model = Kino
        fields = ['tytul', 'cena', 'plakat', 'ranking_imdb', 'data']