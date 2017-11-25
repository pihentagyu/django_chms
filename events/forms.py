from django import forms
from django.contrib.admin import widgets                                       

from dateutil.rrule import *
from django.conf import settings
from .models import *
import pytz

FREQ_CHOICES = (
        (YEARLY, 'Yearly'),
        (MONTHLY, 'Monthly'),
        (WEEKLY, 'Weekly'),
        (DAILY, 'Daily'),
        )

EVENT_TYPE_CHOICES = (
        ('S', 'Simple'),
        ('M', 'Multiple Occurrence'),
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
        initial = {'event_type': 'S'}
        choices = {'event_type': EVENT_TYPE_CHOICES}
#'javascript:handleClick(this);',

class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = ('begin_time', 'end_time')
        #initial = {'begin_time': begin_time, 'end_time': end_time}
    def __init__(self, *args, **kwargs):
        self.begin_time = kwargs.pop('begin_time', None)
        self.end_time = kwargs.pop('end_time', None)
        super(OccurrenceForm, self).__init__(*args, **kwargs)
        if self.begin_time:
            self.fields['begin_time'].initial = pytz.timezone(settings.TIME_ZONE).localize(self.begin_time)
        if self.end_time:
            self.fields['end_time'].initial = pytz.timezone(settings.TIME_ZONE).localize(self.end_time)

        self.fields['begin_time'].widget = widgets.AdminSplitDateTime()
        self.fields['end_time'].widget = widgets.AdminSplitDateTime()

OccurrenceFormset = forms.inlineformset_factory(
        Event, Occurrence,
        form=OccurrenceForm,
        extra=1,
     )

class MultipleOccurrenceForm(forms.Form):
    freq = forms.ChoiceField(
        required=False,
        #widget=forms.Select(attrs = {
        #    'onchange' : 'javascript:handleClick(this);',
        #    }
        #    ),
        choices=FREQ_CHOICES,
        label='Frequency',
    )
    begin_time = forms.TimeField(widget=widgets.AdminTimeWidget)
    end_time = forms.TimeField(widget=widgets.AdminTimeWidget)
    start_day = forms.DateField(widget=widgets.AdminDateWidget)
    end_day = forms.DateField(widget=widgets.AdminDateWidget)



