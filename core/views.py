"""
core/views.py
-------------
Views (controllers) for the Campus Scheduler.

Main goals:
- Signup, login, logout
- Dashboard page
- Create schedule items
- Daily view with date picker (?date=YYYY-MM-DD)
- Weekly grid (Mon-Fri, 8-16)
- Monthly grid (full calendar grid)
"""

from datetime import date, timedelta
import calendar as pycal
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import SignUpForm, ScheduleItemForm
from .models import ScheduleItem
from django.contrib import messages
from django.views.decorators.http import require_POST

# -------------------------
# Auth helpers
# -------------------------

def login_redirect(request):
    """If someone goes to '/', send them to the login page."""
    return redirect("login")


def logout_get_ok(request):
    """
    Log out the user and send them back to login.
    NOTE: This allows logout using GET for simplicity in class projects.
    """
    logout(request)
    return redirect("login")


def signup(request):
    """
    Create a new user account.
    After signup, log the user in automatically.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


# -------------------------
# App pages
# -------------------------

@login_required
def dashboard(request):
    """
    Dashboard page:
    Shows basic actions + upcoming events list.
    """
    upcoming = ScheduleItem.objects.filter(user=request.user).order_by("date", "time")[:10]
    return render(request, "main/dashboard.html", {"upcoming": upcoming})


@login_required
def schedule_create(request):
    """
    Create a schedule item.
    Supports old query string: ?createType=classes or ?createType=work
    """
    initial_type = request.GET.get("createType", "classes")

    if request.method == "POST":
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            # IMPORTANT: redirect to the correct date so user sees it immediately
            return redirect(f"{redirect('calendar_daily').url}?date={item.date.isoformat()}")
    else:
        form = ScheduleItemForm(initial={"item_type": initial_type})

    return render(request, "main/createSchedule.html", {"form": form})


@login_required
def calendar_daily(request):
    """
    Daily calendar view
    - Uses ?date=YYYY-MM-DD, defaults to today
    - Builds 'rows' for hours 0..23 (no KeyError problems)
    - Adds prev/next day navigation
    - Adds week_start for the "Weekly View" jump button
    """
    # 1) Choose date
    chosen_date = parse_date(request.GET.get("date", "")) or date.today()

    # 2) Prev/Next dates for navigation buttons
    prev_date = chosen_date - timedelta(days=1)
    next_date = chosen_date + timedelta(days=1)

    # 3) Monday of the week (for Weekly View jump)
    week_start = chosen_date - timedelta(days=chosen_date.weekday())

    # 4) Load items for the chosen day
    items = ScheduleItem.objects.filter(user=request.user, date=chosen_date).order_by("time")

    # 5) Group items by hour (0..23) so template can render rows safely
    items_by_hour = {h: [] for h in range(24)}
    for item in items:
        # item.time.hour is 0..23
        items_by_hour[item.time.hour].append(item)

    # 6) Build template-friendly rows
    rows = [{"hour": h, "items": items_by_hour[h]} for h in range(24)]

    return render(request, "main/calendarDailyView.html", {
        "chosen_date": chosen_date,
        "prev_date": prev_date,
        "next_date": next_date,
        "week_start": week_start,
        "rows": rows,
    })

@login_required
def calendar_weekly(request):
    """
    Weekly calendar view (Mon–Fri columns, 24-hour rows)
    - Query: ?start=YYYY-MM-DD (any day in the desired week)
    - Normalizes to Monday of that week
    - Builds a grid for the template: table_rows -> [{hour, cells:[{date, items}]}]
    """

    # 1) Read ?start=YYYY-MM-DD (optional)
    start_param = parse_date(request.GET.get("start", ""))

    # 2) Default to this week's Monday if no start is provided
    today = date.today()
    week_start = start_param or (today - timedelta(days=today.weekday()))

    # 3) Normalize to Monday even if the user passed Wed/Thu/etc.
    week_start = week_start - timedelta(days=week_start.weekday())

    # 4) Define full week range (Mon..Sun) and navigation buttons
    week_end = week_start + timedelta(days=6)
    prev_start = week_start - timedelta(days=7)
    next_start = week_start + timedelta(days=7)

    # 5) Days shown in the weekly table header (Mon..Fri)
    week_days = [week_start + timedelta(days=i) for i in range(5)]

    # 6) Show 24 hours (0..23)
    hours = list(range(24))

    # 7) Fetch items for the full week range (Mon..Sun)
    items = ScheduleItem.objects.filter(
        user=request.user,
        date__range=(week_start, week_end)
    ).order_by("date", "time")

    # 8) Map items by (date, hour) for quick grid building
    items_map = {}
    for item in items:
        key = (item.date, item.time.hour)
        items_map.setdefault(key, []).append(item)

    # 9) Build table_rows for template rendering
    table_rows = []
    for h in hours:
        row = {"hour": h, "cells": []}
        for d in week_days:
            row["cells"].append({
                "date": d,
                "items": items_map.get((d, h), [])
            })
        table_rows.append(row)

    # 10) Render with the exact names your template expects
    return render(request, "main/calendarWeeklyView.html", {
        "week_start": week_start,
        "week_end": week_end,
        "week_days": week_days,
        "hours": hours,
        "table_rows": table_rows,
        "prev_start": prev_start,
        "next_start": next_start,
    })
@login_required
def calendar_monthly(request):
    """
    Monthly calendar view
    - Uses ?year=YYYY&month=M
    - Adds Previous/Next month buttons
    - Fetches events for the displayed month
    """
    today = date.today()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # ✅ use pycal (because you imported calendar as pycal)
    last_day = pycal.monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, last_day)

    # Previous month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    # Next month
    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    items = ScheduleItem.objects.filter(
        user=request.user,
        date__range=(start, end)
    ).order_by("date", "time")

    month_matrix = pycal.monthcalendar(year, month)
    month_name = pycal.month_name[month]

    # IMPORTANT: if your template expects month_rows, build it here
    # (you said your template uses month_rows and cell.day/cell.items)
    items_by_day = {}
    for item in items:
        items_by_day.setdefault(item.date.day, []).append(item)

    month_rows = []
    for week in month_matrix:
        week_cells = []
        for day_num in week:
            if day_num == 0:
                week_cells.append({"day": None, "items": []})
            else:
                week_cells.append({"day": day_num, "items": items_by_day.get(day_num, [])})
        month_rows.append(week_cells)

    return render(request, "main/calendarMonthlyView.html", {
        "year": year,
        "month": month,
        "month_name": month_name,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "month_rows": month_rows,   # ✅ matches your template
    })

@login_required
def schedule_detail(request, pk):
    """
    Schedule detail page.
    - Only the owner can view the item
    - Supports ?next=... so the Back button returns to the calendar page
    """
    item = get_object_or_404(ScheduleItem, pk=pk, user=request.user)

    next_url = request.GET.get("next")  # where to go back (daily/weekly/monthly)

    return render(request, "main/scheduleDetail.html", {
        "item": item,
        "next_url": next_url,
    })

@login_required
@require_POST
def schedule_delete(request, pk):
    """
    Delete one schedule item (only if it belongs to the logged-in user).
    Uses POST only for safety.
    """
    item = get_object_or_404(ScheduleItem, pk=pk, user=request.user)

    # Keep where the user came from (daily/weekly/monthly/detail)
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/dashboard/"

    item.delete()
    messages.success(request, "Schedule item removed.")

    return redirect(next_url)