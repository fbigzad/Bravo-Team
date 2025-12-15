from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ScheduleItem(models.Model):
    TYPE_CHOICES = [
        ("classes", "Classes"),
        ("work", "Work"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="classes")
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.title} ({self.item_type}) - {self.date} {self.time}"

    def start_dt(self):
        dt = datetime.combine(self.date, self.time)
        if getattr(settings, "USE_TZ", False):
            return timezone.make_aware(dt, timezone.get_current_timezone())
        return dt

    def end_dt(self):
        return self.start_dt() + timedelta(minutes=self.duration_minutes)

    def clean(self):
        super().clean()

        # If user isn't set yet, skip overlap validation (ModelForm will set it)
        if not self.user_id:
            return

        start = self.start_dt()
        end = self.end_dt()

        qs = ScheduleItem.objects.filter(user=self.user, date=self.date).exclude(pk=self.pk)
        for other in qs:
            if start < other.end_dt() and end > other.start_dt():
                raise ValidationError("This schedule item conflicts with another event.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() runs even outside forms/admin
        return super().save(*args, **kwargs)
