from rest_framework import generics
from ...models  import Kino
from .serializers import KinoSerializer

class KinoListView(generics.ListAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class KinoDetailView(generics.RetrieveAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer