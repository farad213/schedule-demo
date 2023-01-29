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
    path("vacation", views.vacation, name="vacation"),
    path("ajax/vacation_set", views.vacation_set_ajax, name="vacation_set_ajax"),
    path("export_dates", views.export_dates, name="export_dates"),
    path("re_date_project", views.re_date_project, name="re_date_project")
]