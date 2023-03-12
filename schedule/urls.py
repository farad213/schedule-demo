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
    path("re_date_project", views.re_date_project, name="re_date_project"),
    path("repeat_project", views.repeat_project, name="repeat_project"),
    path("SIT_details", views.SIT_details, name="SIT_details"),
    path("ajax/check_SIT", views.check_SIT, name="ajax_check_SIT"),
    path("ajax/user_selection/", views.user_selection, name="user-selection"),
    path("user_selection_date/<int:year>/<int:month>/<int:day>/<int:id>", views.user_selection_date,
         name="user_selection_date"),
    path("ajax/month_change_user_selection", views.month_change_user_selection, name="month_change_user_selection"),
    path("day_nav_user_date", views.day_nav_user_date, name="day_nav_user_date")
]
