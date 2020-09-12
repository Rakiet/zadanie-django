from django.shortcuts import render
from django.http import HttpRequest
from .models import Kino
from .forms import KinoForm

def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    return render(request, 'filmy.html', {'filmy': wszyskie})

def nowy_film(request):
    form = KinoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
    return render(request, 'nowy_film.html', {'form': form})

# Create your views here.
