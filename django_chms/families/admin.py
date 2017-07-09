from datetime import date
from django.contrib import admin

from . import models

class AdultInline(admin.StackedInline):
    model = models.Adult
    max_num = 2
    fieldsets = (
            (None,
                {'fields':('family','title','first_name','middle_name','last_name','suffix','gender','birth_date','marital_status','date_joined','occupation', 'workplace','work_address')}
                ),
            ('Notes',
                {'fields': ('notes',),
                'classes': ('collapse',)}
                )
            )

class ChildInline(admin.StackedInline):
    model = models.Child
    fieldsets = (
        (None,
            {'fields':('family','title','first_name','middle_name','last_name','suffix','gender','birth_date','date_joined','school')}
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
                [d.year, d.year] for d in models.Adult.objects.dates('date_joined', 'year')
                ]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date_joined__year=self.value())

class FamilyAdmin(admin.ModelAdmin):
    inlines = [AdultInline, ChildInline,]
    search_fields = ['family_name']
    list_filter = ['family_name','city']
    list_display = ['family_name']
    fieldsets = (
            (None,
                {'fields':('user','family_name','address1','address2','city','postal_code','state','country')}
                ),
            ('Notes',
                {'fields': ('notes',),
                'classes': ('collapse',)}
                )
            )
    #list_display = ['family_name', 'city', 'time_to_complete']
    #list_editable = ['city']

class AdultAdmin(admin.ModelAdmin):
    #fields = ['family','title','first_name','middle_name','last_name',
    #        'suffix','gender','birth_date','marital_status','date_joined',
    #        'occupation', 'workplace','work_address', 'notes']
    fieldsets = (
            (None,
                {'fields':('family','title','first_name','middle_name','last_name','suffix','gender','birth_date','marital_status','date_joined','occupation', 'workplace','work_address')}
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

class ChildAdmin(admin.ModelAdmin):
    #fields = ['family','title','first_name','middle_name','last_name','suffix',
    #        'gender','birth_date','date_joined','school','notes']
    fieldsets = (
        (None,
            {'fields':('family','title','first_name','middle_name','last_name','suffix','gender','birth_date','date_joined','school')}
            ),
        ('Notes',
            {'fields': ('notes',),
            'classes': ('collapse',)}
            )
        )
    search_fields = ['first_name','last_name']
    list_filter = ['gender','last_name']
    list_display = ['first_name','family', 'last_name', 'age']
    radio_fields = {'gender': admin.VERTICAL}


admin.site.register(models.Family, FamilyAdmin)
#admin.site.register(models.Adult, models.Child)
admin.site.register(models.Adult, AdultAdmin)
admin.site.register(models.Child, ChildAdmin)
