from django.contrib import admin
from . import models

# Register your models here.

class OccurenceInline(admin.StackedInline):
    model = models.Occurrence

class EventAdmin(admin.ModelAdmin):
    model = models.Event
    inlines = (OccurenceInline, )


admin.site.register(models.Event, EventAdmin)
