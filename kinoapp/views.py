from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from .models import Kino
from .forms import KinoForm
from django.contrib.auth.decorators import login_required



def wszystkie_filmy(request):
    wszyskie = Kino.objects.all()
    return render(request, 'filmy.html', {'filmy': wszyskie})

@login_required()
def nowy_film(request):
    form = KinoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect(wszystkie_filmy)
    return render(request, 'film_form.html', {'form': form, 'nowy': True})

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
