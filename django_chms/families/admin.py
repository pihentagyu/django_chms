from django.contrib import admin

from .models import Family, Member

class MemberInline(admin.StackedInline):
    model = Member

class FamilyAdmin(admin.ModelAdmin):
    inlines = [MemberInline,]

admin.site.register(Family, FamilyAdmin)
admin.site.register(Member)
