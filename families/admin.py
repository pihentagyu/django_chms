from datetime import date
from django.contrib import admin

from . import models
from . import forms

class MemberInline(admin.StackedInline):
    model = models.Member
    max_num = 2
    fieldsets = (
            (None,
                {'fields':('family','title','first_name','middle_name','last_name','suffix','gender', 'fam_member_type','birth_date','marital_status','membership_status','date_joined','occupation', 'workplace','work_address', 'school')}
                ),
            ('Notes',
                {'fields': ('notes',),
                'classes': ('collapse',)}
                )
            )

class YearJoinedListFilter(admin.SimpleListFilter):
    title = 'year joined'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return [
                [d.year, d.year] for d in models.Member.objects.dates('date_joined', 'year')
                ]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date_joined__year=self.value())

class FamilyAdmin(admin.ModelAdmin):
    inlines = [MemberInline,]
    search_fields = ['family_name']
    form = forms.FamilyForm
    #list_filter = ['family_name','city']
    #list_display = ['family_name']
    #fieldsets = (
    #        (None,
    #            {'fields':('user','family_name','address1','address2','postal_code','country','region','city','membership_status', 'image')}
    #            ),
    #        ('Notes',
    #            {'fields': ('notes',),
    #            'classes': ('collapse',)}
    #            )
    #        )
    #list_display = ['family_name', 'city', 'time_to_complete']
    #list_editable = ['city']

class MemberAdmin(admin.ModelAdmin):
    #fields = ['family','title','first_name','middle_name','last_name',
    #        'suffix','gender','birth_date','marital_status','membership_status','date_joined',
    #        'occupation', 'workplace','work_address', 'notes']
    fieldsets = (
            (None,
                {'fields':('family','title','first_name','middle_name','last_name','suffix','gender', 'fam_member_type', 'birth_date','marital_status','membership_status','date_joined','occupation', 'workplace','work_address', 'school',)}
                ),
            ('Notes',
                {'fields': ('notes',),
                'classes': ('collapse',)}
                )
            )
    search_fields = ['first_name','last_name']
    list_filter = ['gender','last_name',YearJoinedListFilter]
    list_display = ['first_name', 'family','last_name', 'birth_date', 'date_joined', 'gender']
    radio_fields = {'gender': admin.VERTICAL}


admin.site.register(models.Family, FamilyAdmin)
admin.site.register(models.Member, MemberAdmin)
