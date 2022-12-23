from django.urls import path
from . import views

urlpatterns = [
    path('admin/<int:year>/<int:month>', views.admin, name="admin"),
    path('admin/<int:year>/<int:month>/<int:day>', views.date, name="date"),
    path('ajax/artifacts/', views.artifacts, name='ajax_artifacts'),
    path('ajax/profiles/', views.profiles, name='ajax_profiles'),
    path('calendar/<int:year>/<int:month>', views.user_calendar, name="calendar"),
    path('calendar/<int:year>/<int:month>/<int:day>', views.user_date, name="calendar_date"),
    path('ajax/partial_save/', views.partial_save, name="ajax_partial_save"),
]