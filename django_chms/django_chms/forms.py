from django import forms
from django.core import validators

def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')

class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    suggestions = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput,
            #validators=[validators.MaxLengthValidator(0)],
            validators=[must_be_empty],
            label="Leave empty")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                    "You need to enter same email in both fields"
                    )
        


