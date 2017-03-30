from django.contrib import admin

from . import models

class AdultInline(admin.StackedInline):
    model = models.Adult
    max_num = 2

class DependentInline(admin.StackedInline):
    model = models.Dependent

class FamilyAdmin(admin.ModelAdmin):
    inlines = [AdultInline, DependentInline,]

admin.site.register(models.Family, FamilyAdmin)
admin.site.register(models.Adult)
admin.site.register(models.Dependent)
