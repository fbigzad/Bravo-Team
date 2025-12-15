"""
core/urls.py
------------
URL routes for the Campus Scheduler app.
"""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Home -> login
    path("", views.login_redirect, name="home"),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", views.logout_get_ok, name="logout"),
    path("signup/", views.signup, name="signup"),

    # Pages
    path("dashboard/", views.dashboard, name="dashboard"),
    path("schedule/create/", views.schedule_create, name="schedule_create"),

    # Calendars
    path("calendar/daily/", views.calendar_daily, name="calendar_daily"),
    path("calendar/weekly/", views.calendar_weekly, name="calendar_weekly"),
    path("calendar/monthly/", views.calendar_monthly, name="calendar_monthly"),

    path("schedule/<int:pk>/", views.schedule_detail, name="schedule_detail"),
    path("schedule/<int:pk>/delete/", views.schedule_delete, name="schedule_delete"),

]
