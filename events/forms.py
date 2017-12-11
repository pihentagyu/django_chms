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
        fields = ('start_time', 'end_time', 'all_day')
        #initial = {'start_time': start_time, 'end_time': end_time}
    def __init__(self, *args, **kwargs):
        self.start_time = kwargs.pop('start_time', None)
        self.end_time = kwargs.pop('end_time', None)

        if self.start_time:
            self.start_time = datetime.strptime(self.start_time, '%Y%m%d%H%M')
        if self.end_time:
            self.end_time = datetime.strptime(self.end_time, '%Y%m%d%H%M')
        super(OccurrenceForm, self).__init__(*args, **kwargs)
        if self.start_time:
            self.fields['start_time'].initial = pytz.timezone(settings.TIME_ZONE).localize(self.start_time)
        if self.end_time:
            self.fields['end_time'].initial = pytz.timezone(settings.TIME_ZONE).localize(self.end_time)
        self.fields['start_time'] = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
        self.fields['end_time'] = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
        self.fields['all_day'].initial = False 


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
    start_time = forms.TimeField(widget=widgets.AdminTimeWidget)
    end_time = forms.TimeField(widget=widgets.AdminTimeWidget)
    dtstart = forms.DateField(widget=widgets.AdminDateWidget)
    until = forms.DateField(widget=widgets.AdminDateWidget)

    def add_occurrences(self):
        start_time = self.fields['start_time']
        end_time = self.fields['end_time']
        freq = self.fields['freq']
        print('from recurrent event form'.format(start_time, end_time, freq))
        Event.add_occurrences(self.fields['start_time'], self.fields['end_time'], freq=self.fields['freq'], 
                dtstart=self.fields['begin_date'], until=self.fields['end_date'])



