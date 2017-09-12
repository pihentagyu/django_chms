from django import forms

from . import models

class EventForm(forms.ModelForm):
    
    class Meta:
        model = models.Event

        fields = ('name', 'location', 'group', 'description', 'creator')

class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = models.Occurrence
        fields = ('begin_time', 'end_time')

class OccurrenceFormset = forms.modelformset_factory(
        models.Occurrence,
        form = OccurrenceForm,
        extra=1,
        )


class EventInlineFormset = forms.inlineformset_factory(
        models.Occurrence,
        models.Event,
        fields = ('name', 'location', 'group', 'description', 'creator',)
        formset=OccurrenceFormset,
        max_num=2,
     )
