from datetime import date, timedelta
import calendar

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import SignUpForm, ScheduleItemForm
from .models import ScheduleItem


def login_redirect(request):
    # /index.html should take user to /login/
    return redirect("login")


def logout_get_ok(request):
    # allow logout by GET
    logout(request)
    return redirect("login")


def signup(request):
    # NOTE: your templates are in core/templates/registration/
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    upcoming = ScheduleItem.objects.filter(user=request.user).order_by("date", "time")[:10]
    return render(request, "main/dashboard.html", {"upcoming": upcoming})


@login_required
def schedule_create(request):
    # supports ?createType=classes or ?createType=work
    initial_type = request.GET.get("createType", "classes")

    if request.method == "POST":
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            # Redirect to daily view for the date you just saved (IMPORTANT!)
            return redirect(f"{redirect('calendar_daily').url}?date={item.date.isoformat()}")
    else:
        form = ScheduleItemForm(initial={"item_type": initial_type})

    return render(request, "main/createSchedule.html", {"form": form})


@login_required
def calendar_daily(request):
    # Use ?date=YYYY-MM-DD else default to today
    chosen = parse_date(request.GET.get("date", "")) or date.today()

    items = ScheduleItem.objects.filter(user=request.user, date=chosen).order_by("time")
    return render(request, "main/calendarDailyView.html", {"chosen_date": chosen, "items": items})


@login_required
def calendar_weekly(request):
    # Week starts Monday
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)

    items = ScheduleItem.objects.filter(
        user=request.user,
        date__range=(start, end)
    ).order_by("date", "time")

    return render(request, "main/calendarWeeklyView.html", {"start": start, "end": end, "items": items})


@login_required
def calendar_monthly(request):
    today = date.today()
    year = today.year
    month = today.month

    last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, last_day)

    items = ScheduleItem.objects.filter(
        user=request.user,
        date__range=(start, end)
    ).order_by("date", "time")

    return render(request, "main/calendarMonthlyView.html", {
        "year": year,
        "month": month,
        "start": start,
        "end": end,
        "items": items,
    })
