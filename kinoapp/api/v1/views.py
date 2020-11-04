from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from ...models  import Kino, Bilety, Profile
from .serializers import KinoSerializer, BiletySerializer, ProfileSerializer, UserSerializer, RegisterSerializer, AddProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime, timezone
from rest_framework_simplejwt import authentication



class KinoListView(generics.ListAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class KinoDetailView(generics.RetrieveAPIView):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

class BiletyUserListView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)

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

class AddBiletView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AddProfileSerializer


    def create(self, request):
        # if request.user.is_superuser:
        profile = Profile.objects.create(komentarz=request.data['komentarz'],
                                   user_id=request.data['user'],
                                   bilet_id=request.data['bilet'])
        serializer = AddProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # if request.user.is_superuser:

        profil = self.get_object()
        profil.komentarz=request.data['komentarz']
        profil.save()
        serializer = AddProfileSerializer(profil, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        profil = self.get_object()
        profil.delete()
        return Response('Ticket destroy')

    @action(detail=True, methods=['post'])
    def change_ticket(self, request, *args, **kwargs):

        time_now = datetime.now(timezone.utc)
        profil = self.get_object()
        id_ticket=profil.bilet.id
        ticket = Bilety.objects.filter(id=id_ticket)
        serializerBilet = BiletySerializer(ticket, many=True)
        returnInfo = Response('error')

        if profil.user.id == request.user.id:
            if time_now < profil.bilet.data:
                newTicket = get_object_or_404(Bilety, pk=request.data['bilet'])
                if time_now < newTicket.data:
                    editTicket = self.get_object()
                    editTicket.bilet_id = request.data['bilet']
                    editTicket.save()
                    returnInfo = Response(serializerBilet.data)
                else:
                    returnInfo = Response('new ticket is too old')
            else:
                returnInfo = Response('your ticket is too old')
        else:
            returnInfo = Response('the user is not the owner of the ticket')

        return returnInfo


