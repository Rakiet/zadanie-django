from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Kino, DodatkoweInfo, Ocena, Bilety, Profile
from .forms import KinoForm, DodatkoweInfoForm, OcenaForm, RejestracjaForm, BiletyForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User



def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    bilety = Bilety.objects.all()
    ile = 0
    try:
        user = get_object_or_404(User, pk=request.user.id)
        profile = Profile.objects.filter(user=user)
        for film in profile:
            film.tytul
            ile += 1
    except:
        user:None



    for film in wszyskie:
        for bilet in bilety:
            if bilet.film == film:
                film.bilety_czy_dostepne = True

    return render(request, 'filmy.html', {'filmy': wszyskie, 'bilety': bilety, 'ile_biletow': ile})

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

@login_required()
def kup_bilet(request, id):
    film = get_object_or_404(Kino, pk=id)
    bilet = Bilety.objects.filter(film=film)


    return render(request, 'kup-bilet.html', {'film': film, 'bilety': bilet })


def potwierdz_zakup(request, id):
    bilet = get_object_or_404(Bilety, pk=id)
    form_profile = ProfileForm(request.POST or None)

    if request.method == 'POST':
        if 'tytul' in request.POST:
            profil = form_profile.save(commit=False)
            profil.user = User(id=request.user.id)
            profil.bilet = bilet
            profil.save()
            return redirect(wszystkie_filmy)

    return render(request, 'potwierdz-zakup.html',{'form_profile': form_profile, 'bilet': bilet})


# film = get_object_or_404(Kino, pk=id)
#     oceny = Ocena.objects.filter(film=film)
#
#     form_ocena = OcenaForm(request.POST or None)
#
#     if request.method == 'POST':
#         if 'gwiazdki' in request.POST:
#             ocena = form_ocena.save(commit=False)
#             ocena.film = film
#             ocena.autor = request.user
#             ocena.film = film
#             ocena.save()


# Create your views here.


