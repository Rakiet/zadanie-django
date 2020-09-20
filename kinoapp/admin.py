from django.contrib import admin
from .models import Kino, DodatkoweInfo, Ocena, Bilety, Profile

admin.site.register(Kino)
# Register your models here.
admin.site.register(DodatkoweInfo)
admin.site.register(Ocena)
admin.site.register(Bilety)
admin.site.register(Profile)