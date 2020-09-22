from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class DodatkoweInfo(models.Model):
    GATUNEK = {
        (0, 'Inne'),
        (1, 'Horror'),
        (2, 'Komedia'),
        (3, 'Sci-fi'),
        (4, 'Dramat'),
        (5, 'Akcji'),
    }

    czas_trwania = models.PositiveSmallIntegerField(default=0)
    gatunek = models.PositiveSmallIntegerField(default=0, choices=GATUNEK)


class Kino(models.Model):
    tytul = models.CharField(max_length = 64)
    rok = models.PositiveSmallIntegerField(default=2000)
    opis = models.TextField(default="")
    cena =  models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    plakat = models.ImageField(upload_to='img', null=True, blank=True )
    ranking_imdb =  models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    data = models.DateTimeField(blank=True,null=True)
    dodatkowe = models.OneToOneField(DodatkoweInfo, on_delete=models.CASCADE, blank=True, null=True)
    bilety_czy_dostepne = models.BooleanField(default=False)
    def __str__(self):
        return self.tytul_z_rokiem()

    def tytul_z_rokiem(self):
        return "{} ({})".format(self.tytul, self.rok)

class Ocena(models.Model):
    autor = models.CharField(max_length=64, default='', blank=True)
    CHOICE = [(str(i), i)for i in range(1,11)]
    recenzja = models.TextField(default="", blank=True)
    gwiazdki = models.CharField(default=5,max_length=2,choices=CHOICE)
    film = models.ForeignKey(Kino, on_delete=models.CASCADE)

class Bilety(models.Model):
    data = models.DateTimeField(blank=True, null=True)
    ilosc = models.PositiveSmallIntegerField(default=1)
    film = models.ForeignKey(Kino, on_delete=models.CASCADE)


class Profile(models.Model):

    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    komentarz = models.CharField(max_length=64)
    bilet = models.ForeignKey(Bilety, on_delete=models.CASCADE)

