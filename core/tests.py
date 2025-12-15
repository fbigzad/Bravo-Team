from django.contrib import admin
from .models import ScheduleItem

# Register ScheduleItem so you can view/edit in /admin
@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item_type", "title", "date", "time", "duration_minutes", "created_at")
    list_filter = ("item_type", "date")
    search_fields = ("title", "notes", "user__username")
    ordering = ("-date", "-time")
