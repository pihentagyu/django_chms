from django import forms

from . import models

class FamilyForm(forms.ModelForm):
    class Meta:
        model = models.Family
        fields = [ 'family_name',
                'address1',
                'address2',
                'city',
                'postal_code',
                'state',
                'country',
                'notes',
                ]

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

DependentMemberFormset = forms.modelformset_factory(
        models.Dependent,
        form = DependentMemberForm,
        extra=2,
        )

AdultMemberFormset = forms.modelformset_factory(
        models.Adult,
        form = AdultMemberForm,
        extra=2,
        )

FamilyMemberInlineFormset = forms.inlineformset_factory(
        models.Family,
        models.Adult,
        fields = (
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'suffix',
                'gender',
        ),
        formset=AdultMemberFormset,
        max_num=2,
     )
