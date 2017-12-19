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
            self.start_time = pytz.timezone(settings.TIME_ZONE).localize(self.start_time)
        if self.end_time:
            self.end_time = pytz.timezone(settings.TIME_ZONE).localize(self.end_time)
        super(OccurrenceForm, self).__init__(*args, **kwargs)
        self.fields['start_time'] = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
        self.fields['end_time'] = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
        self.fields['start_time'].initial = self.start_time
        self.fields['end_time'].initial = self.end_time
        self.fields['all_day'].initial = False 

        self.fields['start_time'].required = False
        self.fields['end_time'].required = False
        self.fields['all_day'].required = False 

OccurrenceFormset = forms.inlineformset_factory(
        Event, Occurrence,
        form=OccurrenceForm,
        extra=1,
     )
 
#class RecurringEventForm(forms.ModelForm):
#    freq = forms.ChoiceField(
#        required=False,
#        #widget=forms.Select(attrs = {
#        #    'onchange' : 'javascript:handleClick(this);',
#        #    }
#        #    ),
#        choices=FREQ_CHOICES,
#        label='Frequency',
#    )
#    tstart = forms.TimeField(widget=widgets.AdminTimeWidget)
#    tend = forms.TimeField(widget=widgets.AdminTimeWidget)
#    dtstart = forms.DateField(widget=widgets.AdminDateWidget)
#    until = forms.DateField(widget=widgets.AdminDateWidget)
#    class Meta:
#        model = Event
#        fields = ['name', 'location', 'group', 'event_type', 'description', 'creator']
#        widgets = {'event_type': forms.Select(attrs = {'onchange' : 'javascript:selectEvent()', }) }
#        #initial = {'event_type': 'S'}
#        choices = {'event_type': EVENT_TYPE_CHOICES}
#    def __init__(self, *args, **kwargs):
#        super(RecurringEventForm, self).__init__(*args, **kwargs)
#
#        self.fields['event_type'].initial = 'R'
#
#        self.fields['freq'].required = False
#        self.fields['tstart'].required = False
#        self.fields['tend'].required = False
#        self.fields['dtstart'].required = False 
#        self.fields['until'].required = False 
#
#    def add_occurrences(self):
#        start_time = self.fields['tstart']
#        end_time = self.fields['tend']
#        freq = self.fields['freq']
#        print('from recurrent event form'.format(start_time, end_time, freq))
#        Event.add_occurrences(self.fields['tstart'], self.fields['tend'], freq=self.fields['freq'], 
#                dtstart=self.fields['dtstart'], until=self.fields['until'])

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
    tstart = forms.TimeField(widget=widgets.AdminTimeWidget)
    tend = forms.TimeField(widget=widgets.AdminTimeWidget)
    dtstart = forms.DateField(widget=widgets.AdminDateWidget)
    until = forms.DateField(widget=widgets.AdminDateWidget)

    def __init__(self, *args, **kwargs):
        super(RecurringEventForm, self).__init__(*args, **kwargs)

        self.fields['freq'].required = False
        self.fields['tstart'].required = False
        self.fields['tend'].required = False
        self.fields['dtstart'].required = False 
        self.fields['until'].required = False 

    def add_occurrences(self):
        start_time = self.fields['tstart']
        end_time = self.fields['tend']
        freq = self.fields['freq']
        print('from recurrent event form'.format(start_time, end_time, freq))
        Event.add_occurrences(self.fields['tstart'], self.fields['tend'], freq=self.fields['freq'], 
                dtstart=self.fields['dtstart'], until=self.fields['until'])

