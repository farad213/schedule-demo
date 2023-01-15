from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('buildings', views.buildings, name="buildings"),
    path('buildings/ajax', views.buildings_ajax, name="buildings_ajax"),
    path('jelkod', views.jelkod, name="jelkod"),
    path("jelkod/ajax", views.jelkod_ajax, name="jelkod_ajax"),
    path("quickreport", views.quickreport, name="quickreport")
]

