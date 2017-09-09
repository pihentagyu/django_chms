from django.contrib import admin
from . import models

# Register your models here.

class SimpleEventAdmin(admin.ModelAdmin):
    model = models.SimpleEvent


class SimpleGroupEventAdmin(admin.ModelAdmin):
    model = models.SimpleGroupEvent


class AllDayEventAdmin(admin.ModelAdmin):
    model = models.AllDayEvent


admin.site.register(models.SimpleEvent)
admin.site.register(models.SimpleGroupEvent)
admin.site.register(models.AllDayEvent)
