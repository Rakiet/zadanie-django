from django.urls import path

from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()

router.register(r'test', views.AddBiletView)

urlpatterns = [
    path('kino/', views.KinoListView.as_view(), name='kino_list'),
    path('bilety/', views.BiletyListView.as_view(), name='bilety_list'),
    path('kino/<pk>/', views.KinoDetailView.as_view(), name='kino_detail'),
    path('moje_bilety/', views.BiletyUserListView.as_view(), name='bilety_detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterApi.as_view()),
    url(r'^', include(router.urls))
]