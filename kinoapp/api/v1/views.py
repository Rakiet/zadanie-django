from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from ...models  import Kino, Bilety, Profile
from .serializers import KinoSerializer, BiletySerializer, ProfileSerializer, UserSerializer, RegisterSerializer, AddProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
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



        return profile


class BiletyListView(generics.ListAPIView):
    queryset = Bilety.objects.all()
    serializer_class = BiletySerializer

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class AddBiletView(viewsets.ViewSet):
    queryset = Profile.objects.all()
    serializer_class = AddProfileSerializer


    def create(self, request):
        # if request.user.is_superuser:
        profile = Profile.objects.create(komentarz=request.data['komentarz'],
                                   user_id=request.data['user'],
                                   bilet_id=request.data['bilet'])
        serializer = AddProfileSerializer(profile, many=False)
        return Response(serializer.data)