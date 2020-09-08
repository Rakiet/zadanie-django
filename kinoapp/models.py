from django.db import models

class Kino(models.Model):
    tytul = models.CharField(max_length = 64)