from django.shortcuts import render, get_object_or_404
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
    return render(request, 'film_form.html', {'form': form})

def edytuj_film(reqest, id):
    film = get_object_or_404(Kino, pk=id)
    form = KinoForm(request.POST or None, request.FILES or None, instance=film)

    if form.is_valid():
        form.save()
    return render(request, 'film_form.html', {'form': form})
# Create your views here.
