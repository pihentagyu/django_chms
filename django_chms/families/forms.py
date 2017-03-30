from django import forms

from . import models

class AdultMemberForm(forms.ModelForm):
    class Meta:
        model = models.Adult
        fields = [
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'gender',
                'occupation',
                ]

class DependentMemberForm(forms.ModelForm):
    class Meta:
        model = models.Dependent
        fields = [
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'gender',
                ]
