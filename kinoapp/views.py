from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Kino, DodatkoweInfo, Ocena, Bilety
from .forms import KinoForm, DodatkoweInfoForm, OcenaForm, RejestracjaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required




def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    bilety = Bilety.objects.all()

    for film in wszyskie:
        for bilet in bilety:
            if bilet.film == film:
                film.bilety_czy_dostepne = True

    return render(request, 'filmy.html', {'filmy': wszyskie, 'bilety': bilety})

@staff_member_required
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

@staff_member_required
def edytuj_film(request, id):
    film = get_object_or_404(Kino, pk=id)

    try:
        dodatkowe = DodatkoweInfo.objects.get(pk=film.id)
    except DodatkoweInfo.DoesNotExist:
        dodatkowe = None

    form_film = KinoForm(request.POST or None, request.FILES or None, instance=film)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None, instance=dodatkowe)

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form_film, 'form_dodatkowe': form_dodatkowe, 'nowy': False})

@staff_member_required
def usun_film(request, id):
    film = get_object_or_404(Kino, pk=id)

    if request.method == "POST":
        film.delete()
        return redirect(wszystkie_filmy)

    return render(request, 'potwierdz.html', {'film': film})

def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(wszystkie_filmy)
    else:
        form = RejestracjaForm()
    return render(request, 'rejestracja.html', {'form': form})

@login_required()
def ocen_film(request, id):
    film = get_object_or_404(Kino, pk=id)
    oceny = Ocena.objects.filter(film=film)

    form_ocena = OcenaForm(request.POST or None)

    if request.method == 'POST':
        if 'gwiazdki' in request.POST:
            ocena = form_ocena.save(commit=False)
            ocena.film = film
            ocena.autor = request.user
            ocena.film = film
            ocena.save()




    return render(request, 'ocen.html', {'film': film, 'oceny': oceny, 'form_ocena': form_ocena})

# Create your views here.


