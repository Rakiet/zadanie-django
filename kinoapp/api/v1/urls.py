from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('kino/', views.KinoListView.as_view(), name='kino_list'),
    path('bilety/', views.BiletyListView.as_view(), name='bilety_list'),
    path('kino/<pk>/', views.KinoDetailView.as_view(), name='kino_detail'),
    path('moje_bilety/', views.BiletyUserListView.as_view(), name='bilety_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


]