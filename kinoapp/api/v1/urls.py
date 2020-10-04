from django.urls import path
from . import views

urlpatterns = [
    path('kino/', views.KinoListView.as_view(), name='kino_list'),
    path('bilety/', views.BiletyListView.as_view(), name='bilety_list'),
    path('kino/<pk>/', views.KinoDetailView.as_view(), name='kino_detail')

]