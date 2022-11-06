from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('buildings', views.buildings, name="buildings"),
    path('jelkod', views.jelkod, name="length_calc"),
]