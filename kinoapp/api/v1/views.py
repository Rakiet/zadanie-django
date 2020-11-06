from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ...models  import Kino, Bilety, Profile, Ocena
from .serializers import KinoSerializer, BiletySerializer, ProfileSerializer, UserSerializer, RegisterSerializer, AddProfileSerializer, RatingSerializer
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

class AddRatingView(viewsets.ModelViewSet):
    queryset = Ocena.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        movie = Kino.objects.filter(id=request.data['film_id'])
        if not movie:
            return Response('the movie does not exist')

        elif(request.data['gwiazdki'] > 10 or request.data['gwiazdki'] < 1):

            return Response('the score must be 1 to 10')
        else:
            rating = Ocena.objects.create(autor=request.user.username,
                                        recenzja=request.data['recenzja'],
                                        gwiazdki=request.data['gwiazdki'],
                                        film_id=request.data['film_id'])
            serializer = RatingSerializer(rating, many=False)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        rating = self.get_object()
        if rating.autor == request.user.username:
            rating.recenzja=request.data['recenzja']
            rating.gwiazdki = request.data['gwiazdki']
            rating.save()
            serializer = RatingSerializer(rating, many=False)
            return Response(serializer.data)
        else:
            return Response('the user is not the owner of the rating')

    def destroy(self, request, *args, **kwargs):
        rating = self.get_object()
        if rating.autor == request.user.username:
            rating.delete()
            return Response('Rating destroy')
        else:
            return Response('the user is not the owner of the rating')


class AddBiletView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AddProfileSerializer


    def create(self, request):
        ticket = Bilety.objects.filter(id=request.data['bilet'])
        if not ticket:
            return Response('the ticket does not exist')
        else:
            profile = Profile.objects.create(komentarz=request.data['komentarz'],
                                       user_id=request.user.id,
                                       bilet_id=request.data['bilet'])
            serializer = AddProfileSerializer(profile, many=False)
            return Response(serializer.data)




    def update(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        profil = self.get_object()
        if profil.user.id == request.user.id:
            profil.komentarz=request.data['komentarz']
            profil.save()
            serializer = AddProfileSerializer(profil, many=False)
            return Response(serializer.data)
        else:
            return Response('the user is not the owner of the ticket')

    def destroy(self, request, *args, **kwargs):
        profil = self.get_object()
        if profil.user.id == request.user.id:
            profil.delete()
            return Response('Ticket destroy')
        else:
            return Response('the user is not the owner of the ticket')

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


