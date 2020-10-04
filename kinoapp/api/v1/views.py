from rest_framework import generics, viewsets
from ...models  import Kino, Bilety
from .serializers import KinoSerializer, BiletySerializer

class KinoListView(generics.ListAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class KinoDetailView(generics.RetrieveAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer



class BiletyListView(generics.ListAPIView):
    queryset = Bilety.objects.all()
    serializer_class = BiletySerializer