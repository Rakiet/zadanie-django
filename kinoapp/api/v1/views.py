from rest_framework import generics, viewsets
from ...models  import Kino, Bilety, Profile
from .serializers import KinoSerializer, BiletySerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from datetime import datetime, timezone

class KinoListView(generics.ListAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class KinoDetailView(generics.RetrieveAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class BiletyUserListView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=2)

        profile = Profile.objects.filter(user=user)
        data_teraz = datetime.now(timezone.utc)



        return profile


class BiletyListView(generics.ListAPIView):
    queryset = Bilety.objects.all()
    serializer_class = BiletySerializer