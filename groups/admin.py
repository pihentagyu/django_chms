from django.contrib import admin
from . import models

# Register your models here.
class MemberInline(admin.StackedInline):
    model = models.GroupMember

class GroupAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)
    model = models.Group

admin.site.register(models.GroupMember)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupType)
admin.site.register(models.MemRole)

