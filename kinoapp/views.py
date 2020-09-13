from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from .models import Kino
from .forms import KinoForm, DodatkoweInfo, Ocena
from django.contrib.auth.decorators import login_required



def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    return render(request, 'filmy.html', {'filmy': wszyskie})

@login_required()
def nowy_film(request):
    form_film = KinoForm(request.POST or None, request.FILES or None)
    form_dodatkowy = DodatkoweInfo(request.POST or None)
    form_ocena = Ocena(request.POST or None)

    if all((form_film.is_valid(), form_ocena.is_valid(), form_dodatkowy.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowy.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form_film, 'form_dodatkowy': form_dodatkowy, 'form_ocena': form_ocena, 'nowy': True})

@login_required()
def edytuj_film(request, id):
    film = get_object_or_404(Kino, pk=id)
    form = KinoForm(request.POST or None, request.FILES or None, instance=film)

    if form.is_valid():
        form.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form, 'nowy': False})

@login_required()
def usun_film(request, id):
    film = get_object_or_404(Kino, pk=id)

    if request.method == "POST":
        film.delete()
        return redirect(wszystkie_filmy)

    return render(request, 'potwierdz.html', {'film': film})

# Create your views here.
