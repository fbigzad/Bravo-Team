"""
core/admin.py
-------------
Registers models with Django Admin so you can manage data easily.
"""

from django.contrib import admin
from .models import ScheduleItem


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduleItem.
    - list_display: which columns show in admin list view
    - list_filter: quick filters on the right side
    - search_fields: search bar fields
    """
    list_display = ("user", "item_type", "title", "date", "time", "duration_minutes", "created_at")
    list_filter = ("item_type", "date")
    search_fields = ("title", "notes", "user__username")
    ordering = ("-date", "-time")
