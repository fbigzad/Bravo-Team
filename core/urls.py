from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path("", views.dashboard, name="dashboard"),
    path("schedule/create/", views.schedule_create, name="schedule_create"),
    path("calendar/daily/", views.calendar_daily, name="calendar_daily"),
    path("calendar/weekly/", views.calendar_weekly, name="calendar_weekly"),
    path("calendar/monthly/", views.calendar_monthly, name="calendar_monthly"),

    # Compatibility routes (so your old links like dashboard.html still work)
    path("index.html", views.login_redirect),
    path("dashboard.html", views.dashboard),
    path("signUp.html", views.signup),  # handles GET/POST
    path("createSchedule.html", views.schedule_create),
    path("calendarDailyView.html", views.calendar_daily),
    path("calendarWeeklyView.html", views.calendar_weekly),
    path("calendarMonthlyView.html", views.calendar_monthly),
]