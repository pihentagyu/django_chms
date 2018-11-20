from dal import autocomplete
from datetime import date
from django import forms

from . import models
from cities_local.models import Country, Region, City

class FamilyForm(forms.ModelForm):
    country = forms.ModelChoiceField(
            queryset=Country.objects.all(),
            widget=autocomplete.ModelSelect2(url='cities_local:country_autocomplete')
            )
    region = forms.ModelChoiceField(
            queryset=Region.objects.all(),
            widget=autocomplete.ModelSelect2(url='cities_local:region_autocomplete', forward=('country',))
            )
    city = forms.ModelChoiceField(
            queryset=City.objects.all(),
            widget=autocomplete.ModelSelect2(url='cities_local:city_autocomplete', forward=('Region',))
            )
    class Meta:
        model = models.Family
        #fields = ('user', 'family_name', 'address1', 'address2', 'city', 'postal_code', 'region', 'country', 'notes')
        fields = ['user',
                'family_name',
                'address1',
                'address2',
                'country',
                'region',
                'city',
                'postal_code',
                'notes',
                'image',
                ]
        widgets = {'image': forms.widgets.ClearableFileInput}

class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = [
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'fam_member_type',
                'gender',
                'birth_date', 
                'marital_status', 
                'date_joined', 
                'occupation',
                'workplace', 
                'school',
                'work_address', 
                'notes'
                ]

        widgets = {'birth_date': forms.widgets.SelectDateWidget(years=[y for y in range(date.today().year, date.today().year-110, -1)]), 'date_joined': forms.widgets.SelectDateWidget(years=[y for y in range(date.today().year, date.today().year-110, -1)])}
        #fields = ('title', 'first_name', 'last_name', 'suffix', 'fam_member_type', 'gender', 'birth_date', 
        #        'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address', 'school', 'notes')
MemberFormset = forms.modelformset_factory(
        models.Member,
        form = MemberForm,
        extra=2,
        )

FamilyMemberInlineFormset = forms.inlineformset_factory(
        models.Family,
        models.Member,
        fields = (
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'gender',
                'fam_member_type',
        ),
        formset=MemberFormset,
        max_num=2,
     )
