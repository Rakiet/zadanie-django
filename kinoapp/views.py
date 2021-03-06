from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Kino, DodatkoweInfo, Ocena, Bilety, Profile
from .forms import KinoForm, DodatkoweInfoForm, OcenaForm, RejestracjaForm, BiletyForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.db.models import Count
import operator



def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    bilety = Bilety.objects.all()
    ile = 0
    try:
        user = get_object_or_404(User, pk=request.user.id)
        profile = Profile.objects.filter(user=user)
        ile = len(profile)
    except:
        user:None


    dostepne = Bilety.objects.values('film', 'film__tytul', 'film__opis', 'film__plakat').annotate(Count('film'))


    return render(request, 'filmy.html', { 'bilety': bilety, 'ile_biletow': ile, 'dostepne': dostepne})

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
    bilet = Ocena.objects.filter(film=film)

    try:
        dodatkowe = DodatkoweInfo.objects.get(pk=film.id)
    except DodatkoweInfo.DoesNotExist:
        dodatkowe = None

    form_film = KinoForm(request.POST or None, request.FILES or None, instance=film)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None, instance=dodatkowe)
    form_bilet = BiletyForm(request.POST or None)

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)

    if request.method == 'POST':
        if 'ilosc' in request.POST:
            bilet = form_bilet.save(commit=False)
            bilet.film = film
            bilet.save()

    return render(request, 'film_form.html', {'form': form_film, 'form_bilet': form_bilet, 'form_dodatkowe': form_dodatkowe, 'nowy': False})

@staff_member_required
def usun_film(request, id):
    film = get_object_or_404(Kino, pk=id)

    if request.method == "POST":
        film.delete()
        return redirect(wszystkie_filmy)

    return render(request, 'potwierdz.html', {'film': film, 'usun_bilet': False})

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

@login_required()
def kup_bilet(request, id):
    film = get_object_or_404(Kino, pk=id)
    bilet = Bilety.objects.filter(film=film)


    return render(request, 'kup-bilet.html', {'film': film, 'bilety': bilet, 'wymiana_biletu': False})


def potwierdz_zakup(request, id):
    bilet = get_object_or_404(Bilety, pk=id)
    form_profile = ProfileForm(request.POST or None)

    if request.method == 'POST':
        if 'komentarz' in request.POST:
            profil = form_profile.save(commit=False)
            profil.user = User(id=request.user.id)
            profil.bilet = bilet
            profil.save()
            return redirect(wszystkie_filmy)

    return render(request, 'potwierdz-zakup.html',{'form_profile': form_profile, 'bilet': bilet})

@login_required()
def moje_bilety(request):
    user = get_object_or_404(User, pk=request.user.id)
    profile = Profile.objects.filter(user=user)
    pro = []
    data_teraz = datetime.now(timezone.utc)

    for profil in profile:
        if profil.bilet.data > data_teraz:
            pro.append((Bilety.objects.filter(film=profil.bilet.film),profil))
        else:
            pro.append(((), profil))


    return render(request, 'moje_bilety.html', {'profile': pro, 'data_teraz': data_teraz})

@login_required()
def potwierdz_wymiane(request, profil_id, seans_id):
    profil = get_object_or_404(Profile, pk=profil_id)
    bilet = get_object_or_404(Bilety, pk=seans_id)

    if request.method == "POST":

        profil.bilet = Bilety(id=seans_id)
        profil.save()
        return redirect(moje_bilety)


    return render(request, 'potwierdz_wymiane.html', {'profil': profil, 'bilet': bilet})

@login_required()
def usun_bilet(request, id):
    profil = get_object_or_404(Profile, pk=id)

    if request.method == "POST":
        profil.delete()
        return redirect(moje_bilety)

    return render(request, 'potwierdz.html', {'profil': profil, 'usun_bilet': True})







