from datetime import date, datetime
from dateutil import rrule
from django.core.urlresolvers import reverse
from django.db import models

from families.models import Member
from groups.models import Group

# Create your models here.
EVENT_TYPE_CHOICES = (
        ('S', 'Simple'),
        ('R', 'Recurring Event'),
        ('H', 'Holiday'),
        )


class Location(models.Model):
    name = models.CharField(max_length=35)
    building = models.CharField(max_length=35)
    description = models.CharField(blank=True, null=True, max_length=255)


class Event(models.Model):
    name = models.CharField(max_length=35)
    event_type = models.CharField(choices=EVENT_TYPE_CHOICES, max_length=1)
    description = models.CharField(blank=True, null=True, max_length=255)
    creator = models.ForeignKey(Member)
    group = models.ForeignKey(Group, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={
            'pk': self.id,
            })

    def __str__(self):
        return self.name

    ## From django-swingtime
    def add_occurrences(self, start_time, end_time, event_type, **kwargs):


        '''
        Add one or more occurences to the event using a comparable API to 
        ``dateutil.rrule``. 
        
        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.
        
        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.
        
        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        '''
        # freq = kwarg.pop('freq', None)
        # dtstart = kwarg.pop('dtstart', None)
        # interval = kwarg.pop('interval', None)
        # wkst = kwarg.pop('wkst', None)
        # count = kwarg.pop('count', None)
        # until = kwarg.pop('until', None)
        # bysetpos = kwarg.pop('bysetpos', None)
        # bymonth = kwarg.pop('bymonth', None)
        # bymonthday = kwarg.pop('bymonthday', None)
        # byyearday = kwarg.pop('byyearday', None)
        # byweekno = kwarg.pop('byweekno', None)
        # byweekday = kwarg.pop('byweekday', None)
        # byeaster = kwarg.pop('byeaster', None)
        # start_time = kwarg.pop('start_time', None)
        # end_time = kwarg.pop('end_time', None)
        # count = kwarg.pop('count', None)
        # until = kwarg.pop('until', None)
        if all_day == True:
            start_time, end_time = Occurrence.set_all_day_times(start_time)

        if event_type == 'S':
            self.occurrence_set.create(event=self, start_time=start_time, end_time=end_time, **kwargs)


        if not (kwargs.get(count) and not kwargs.get(until)):
            year = timedelta(365)
            if freq == rrule.YEARLY:
                kwargs['until'] = kwargs['dtstart'] + 25 * year # Add 25 years in occurrence table
            elif freq == rrule.MONTHLY:
                kwargs['until'] = kwargs['dtstart'] + 25 * year # Add 25 years in occurrence table
            elif freq == rrule.WEEKLY:
                kwargs['until'] = kwargs['dtstart'] + 15 * year # Add 25 years in occurrence table
            elif freq == rrule.DAILY:
                kwargs['until'] = kwargs['dtstart'] + 10 * year # Add 25 years in occurrence table

            occurrences = [[Occurrence(event=self, start_time=occurrence, end_time=occurrence+delta, notes=None, all_day=all_day)] for occurrence in rrule.rrule(**rrule_kwargs)]
            self.occurrence_set.bulk_create(occurrences)

            dtstart = until
            until = None
            self.calculatedoccurrence_set.create(event=self, start_time=start_time, end_time=end_time, **kwargs)
                
        else:
            rrule_params.setdefault('freq', rrule.DAILY)
            delta = end_time - start_time
            occurrences = []
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                occurrences.append(Occurrence(start_time=ev, end_time=ev + delta, event=self))
            self.occurrence_set.bulk_create(occurrences)

    def get_occurrences(self, start_time, end_time, **kwargs):
        occurrence_type = kwargs.pop('type', None)
        if occurrence_type == 'recurring':
            '''get recurring only'''
            return 'recurring'
        elif occurrence_type == 'simple':
            '''get simple occurrences only'''
            return 'simple'
        else:
            return 'all'

        pass


class Occurrence(models.Model):
    event = models.ForeignKey(Event)
    notes = models.CharField(blank=True, null=True, max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    all_day = models.BooleanField()

    def get_duration(self):
        from events.templatetags.event_extras import duration_calc
        return duration_calc(self.start_time, self.end_time)

    def set_all_day_times(self, start_time):
        if self.all_day == True:
            start_time = datetime.combine(start_time, datetime.min.time())
            end_time = datetime.combine(start_time, datetime.max.time())
            return start_time, end_time

'''
rrule parameters from documentation:
freq    must be one of YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, or SECONDLY. 
cache   If given, it must be a boolean value specifying to enable or disable caching of results. If you will use the same rrule instance multiple times, enabling caching will improve the performance considerably. 
dtstart The recurrence start. Besides being the base for the recurrence, missing parameters in the final recurrence instances will also be extracted from this date. If not given, datetime.now() will be used instead. 
interval The interval between each freq iteration. For example, when using YEARLY, an interval of 2 means once every two years, but with HOURLY, it means once every two hours. The default interval is 1. 
wkst The week start day. Must be one of the MO, TU, WE constants, or an integer, specifying the first day of the week. This will affect recurrences based on weekly periods. The default week start is got from calendar.firstweekday(), and may be modified by calendar.setfirstweekday(). 
count How many occurrences will be generated. 
until If given, this must be a datetime instance, that will specify the limit of the recurrence. If a recurrence instance happens to be the same as the datetime instance given in the until keyword, this will be the last occurrence. 
bysetpos If given, it must be either an integer, or a sequence of integers, positive or negative. Each given integer will specify an occurrence number, corresponding to the nth occurrence of the rule inside the frequency period. For example, a bysetpos of -1 if combined with a MONTHLY frequency, and a byweekday of (MO, TU, WE, TH, FR), will result in the last work day of every month. 
bymonth If given, it must be either an integer, or a sequence of integers, meaning the months to apply the recurrence to. 
bymonthday If given, it must be either an integer, or a sequence of integers, meaning the month days to apply the recurrence to. 
byyearday If given, it must be either an integer, or a sequence of integers, meaning the year days to apply the recurrence to. 
byweekno If given, it must be either an integer, or a sequence of integers, meaning the week numbers to apply the recurrence to. Week numbers have the meaning described in ISO8601, that is, the first week of the year is that containing at least four days of the new year. 
byweekday If given, it must be either an integer (0 == MO), a sequence of integers, one of the weekday constants (MO, TU, etc), or a sequence of these constants. When given, these variables will define the weekdays where the recurrence will be applied. It's also possible to use an argument n for the weekday instances, which will mean the nth occurrence of this weekday in the period. For example, with MONTHLY, or with YEARLY and BYMONTH, using FR(+1) in byweekday will specify the first friday of the month where the recurrence happens. Notice that in the RFC documentation, this is specified as BYDAY, but was renamed to avoid the ambiguity of that keyword. 
byhour If given, it must be either an integer, or a sequence of integers, meaning the hours to apply the recurrence to. 
byminute If given, it must be either an integer, or a sequence of integers, meaning the minutes to apply the recurrence to. 
bysecond If given, it must be either an integer, or a sequence of integers, meaning the seconds to apply the recurrence to. 
byeaster If given, it must be either an integer, or a sequence of integers, positive or negative. Each integer will define an offset from the Easter Sunday. Passing the offset 0 to byeaster will yield the Easter Sunday itself. This is an extension to the RFC specification. 

'''

class CalculatedOccurrence(models.Model):
    event = models.ForeignKey(Event)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    freq = models.IntegerField()
    dtstart = models.DateField()
    interval = models.IntegerField(default=1)
    wkst = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)
    bysetpos = models.CharField(max_length=255, blank=True, null=True)
    bymonth = models.CharField(max_length=255, blank=True, null=True)
    bymonthday = models.CharField(max_length=255, blank=True, null=True)
    byyearday = models.CharField(max_length=255, blank=True, null=True)
    byweekno = models.CharField(max_length=255, blank=True, null=True)
    byweekday = models.CharField(max_length=255, blank=True, null=True)
    byeaster = models.CharField(max_length=255, blank=True, null=True)


#class AllDayEvent(Event):
#    date = models.DateField()
#
#    def get_start_time(self):
#        return datetime.combine(date, datetime.min.time())
#
#    def get_end_time(self):
#        return datetime.combine(date, datetime.max.time())
#
