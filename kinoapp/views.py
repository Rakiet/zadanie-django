from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Kino, DodatkoweInfo, Ocena
from .forms import KinoForm, DodatkoweInfoForm, OcenaForm
from django.contrib.auth.decorators import login_required



def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    return render(request, 'filmy.html', {'filmy': wszyskie})

@login_required()
def nowy_film(request):
    form_film = KinoForm(request.POST or None, request.FILES or None)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None)

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form_film, 'form_dodatkowe': form_dodatkowe, 'nowy': True})

@login_required()
def edytuj_film(request, id):
    film = get_object_or_404(Kino, pk=id)
    oceny = Ocena.objects.filter(film=film)

    try:
        dodatkowe = DodatkoweInfo.objects.get(pk=film.id)
    except DodatkoweInfo.DoesNotExist:
        dodatkowe = None

    form_film = KinoForm(request.POST or None, request.FILES or None, instance=film)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None, instance=dodatkowe)
    form_ocena = OcenaForm(request.POST or None)

    if request.method == 'POST':
        if 'gwiazdki' in request.POST:
            ocena = form_ocena.save(commit=False)
            ocena.film = film
            ocena.save()

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form_film, 'form_dodatkowe': form_dodatkowe, 'oceny': oceny, 'form_ocena': form_ocena, 'nowy': False,})

@login_required()
def usun_film(request, id):
    film = get_object_or_404(Kino, pk=id)

    if request.method == "POST":
        film.delete()
        return redirect(wszystkie_filmy)

    return render(request, 'potwierdz.html', {'film': film})

# Create your views here.
