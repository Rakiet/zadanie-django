from django.db import models

class Kino(models.Model):
    tytul = models.CharField(max_length = 64)
    rok = models.PositiveSmallIntegerField(default=2000)
    opis = models.TextField(default="")
    cena =  models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    plakat = models.ImageField(upload_to = "img", null=True, blank=True )
    ranking_imdb =  models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    data = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.tytul_z_rokiem()

    def tytul_z_rokiem(self):
        return "{} ({})".format(self.tytul, self.rok)