from django.contrib import admin

# Register your models here.

from django.contrib import admin
from . import models

class AdultInline(admin.StackedInline):
    model = models.GroupAdultMember

class ChildInline(admin.StackedInline):
    model = models.GroupChildMember

class MemberAdmin(admin.ModelAdmin):
    #list_display = ('last_name', 'first_name')
    inlines = [AdultInline, ChildInline]
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    inlines = [AdultInline, ChildInline,]
    search_fields = ['group_name']

admin.site.register(models.Group, MemberAdmin)
admin.site.register(models.GroupType)
admin.site.register(models.GroupAdultMember)
admin.site.register(models.GroupChildMember)
admin.site.register(models.MemRole)

