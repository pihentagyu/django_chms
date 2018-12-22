#from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.contrib.admin import widgets                                       

from dateutil import rrule
from django.conf import settings
#from djangoformsetjs.utils import formset_media_js
from bootstrap_datepicker_plus import DateTimePickerInput

from .models import *
import pytz


FREQ_CHOICES = (
        (rrule.DAILY, 'Daily'),
        (rrule.WEEKLY, 'Weekly'),
        (rrule.MONTHLY, 'Monthly'),
        (rrule.YEARLY, 'Yearly'),
        )

EVENT_TYPE_CHOICES = (
        ('S', 'Simple'),
        ('R', 'Recurring Event'),
        )

WEEK_START = settings.WEEK_START_DAY

class EventForm(forms.ModelForm):
    #event_type = forms.ChoiceField(
    #        choices=EVENT_TYPE_CHOICES, 
    #        widget=forms.Select(attrs = {
    #            'onchange' : 'refresh();',
    #        }
    #        ),
    #    )
    #def __init__(self, *args, **kwargs):
    #    super(EventForm, self).__init__(*args, **kwargs)
    #    self.fields['event_type'].widget = forms.Select(attrs = {'onchange' : "alert('foo');"}, ) 
    class Meta:
        model = Event
        fields = ['name', 'location', 'group', 'event_type', 'description', 'creator']
        widgets = {'event_type': forms.Select(attrs = {'onchange' : 'javascript:selectEvent()', }) }
        #initial = {'event_type': 'S'}
        choices = {'event_type': EVENT_TYPE_CHOICES}
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].initial = 'S'

#'javascript:handleClick(this);',

class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = ('start_time', 'end_time', 'notes', 'all_day', 'multi_day')
        widgets = {
                'start_time': DateTimePickerInput(
                    options={'inline': True, 'stepping': 15}
                        ), #options={'format' : "YYYY-MM-DD HH:mm", 'stepping': 15, 'inline': True }), 
                'end_time': DateTimePickerInput(
                    options={'inline': True, 'stepping': 15}
                        ), #options={'format' : "YYYY-MM-DD HH:mm", 'stepping': 15, 'inline': True }), 
                    }
        #initial = {'start_time': start_time, 'end_time': end_time}
        #widgets = {'start_time': forms.widgets.DateTimeInput(attrs={'class':'timepicker'}), 
        #        'end_time': forms.widgets.DateTimeInput(attrs={'class':'timepicker'})
        #        }
    def __init__(self, *args, **kwargs):
        self.start_time = kwargs.pop('start_time', None)
        self.end_time = kwargs.pop('end_time', None)
        #if self.start_time:
        #    self.start_time = pytz.timezone(settings.TIME_ZONE).localize(self.start_time)
        #if self.end_time:
        #    self.start_time = pytz.timezone(settings.TIME_ZONE).localize(self.start_time)
        super(OccurrenceForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].initial = self.start_time
        self.fields['end_time'].initial = self.end_time
        self.fields['all_day'].initial = False 
        self.fields['multi_day'].initial = False 

        self.fields['start_time'].required = False
        self.fields['end_time'].required = False
        self.fields['notes'].required = False
        self.fields['all_day'].required = False 
        self.fields['multi_day'].required = False 
    #class Media(object):
    #    js = formset_media_js

OccurrenceFormset = forms.inlineformset_factory(
        Event, Occurrence,
        form=OccurrenceForm,
        extra=1,
     )

class RecurringEventForm(forms.Form):
    freq = forms.ChoiceField(
        required=False,
        #widget=forms.Select(attrs = {
        #    'onchange' : 'javascript:handleClick(this);',
        #    }
        #    ),
        choices=FREQ_CHOICES,
        label='Frequency',
    )
    start_time = forms.DateTimeField(
            widget=DateTimePickerInput(
                options={'format' : "YYYY-MM-DD HH:mm", 'stepping': 15, 'inline': True}
                )
            )
    duration = forms.DurationField(
            widget=forms.TextInput(
                attrs={'placeholder':'00:30'}
                )
            )
    until = forms.DateTimeField(widget=DateTimePickerInput(
                options={'format' : "YYYY-MM-DD HH:mm", 'stepping': 15, 'inline': True}
        )
        )
    #until = forms.DateField(widget=widgets.AdminDateWidget)

    def __init__(self, *args, **kwargs):
        super(RecurringEventForm, self).__init__(*args, **kwargs)

        self.fields['freq'].required = False
        self.fields['start_time'].required = False 
        self.fields['until'].required = False 
        self.fields['duration'].required = False 

    def add_occurrences(self, **kwargs):
        Event.add_occurrences(**kwargs)

