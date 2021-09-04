from datetime import date, datetime, timedelta
from dateutil import rrule
from django.urls import reverse_lazy
from django.db import models

from events.templatetags.event_extras import duration_calc
from families.models import Member
from groups.models import Group

EVENT_TYPE_CHOICES = (
        ('S', 'Simple'),
        ('R', 'Recurring Event'),
        ('H', 'Holiday'),
        )

CALENDAR_TYPE_CHOICES = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
        )

class Calendar(models.Model):
    calendar_type = models.CharField(choices=CALENDAR_TYPE_CHOICES, max_length=1)
    year = models.IntegerField()
    month = models.CharField(max_length=2, blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)

class Location(models.Model):
    name = models.CharField(max_length=35)
    building = models.CharField(max_length=35)
    description = models.CharField(blank=True, null=True, max_length=255)

#class EventManager(models.Manager):
#    def create_event(self, name, event_type, description, creator, group, location): #, start_time, end_time, event_type, **kwargs):
#        event = self.create(name=name, event_type=event_type, description=description, creator=creator, group=group, location=location)
#    #def add_event_occurrences(start
#    #    occurrences = self.add_occurrences(start_time, end_time, **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=35)
    event_type = models.CharField(choices=EVENT_TYPE_CHOICES, max_length=1)
    description = models.CharField(blank=True, null=True, max_length=255)
    creator = models.ForeignKey(Member, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse_lazy('events:event_detail', kwargs={
            'pk': self.id,
            })

    def __str__(self):
        return self.name

    ## From django-swingtime
    def add_occurrences(self, **kwargs):

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

        # freq
        # dtstart
        # interval
        # wkst
        # count
        # until
        # bysetpos
        # bymonth
        # bymonthday
        # byyearday
        # byweekno
        # byweekday
        # byeaster

        freq = int(kwargs.pop('freq'))
        all_day = kwargs.pop('all_day', False)
        duration = kwargs.pop('duration')
        start_time = kwargs.pop('start_time')
        end_time = start_time + duration
        if all_day == True:
            #duration = Occurrence.set_all_day_times(start_time)
            duration = timedelta(days=1)

        #if (kwargs.get('count') or kwargs.get('until')):
        #    kwargs.setdefault('freq', rrule.DAILY)
        #    #occurrences = []
        #    #for ev in rrule.rrule(**kwargs):
        #    #    occurrences.append(Occurrence(event=self, start_time=ev, duration=duration, notes=None, all_day=all_day))
        #    #self.occurrence_set.bulk_create(occurrences)
        if kwargs.get('until', None) == None:
            year = timedelta(365)
            if freq == rrule.YEARLY:
                kwargs['until'] = kwargs['dtstart'] + 25 * year # Add 25 years in occurrence table
            elif freq == rrule.MONTHLY:
                kwargs['until'] = kwargs['dtstart'] + 25 * year # Add 25 years in occurrence table
            elif freq == rrule.WEEKLY:
                kwargs['until'] = kwargs['dtstart'] + 15 * year # Add 25 years in occurrence table
            elif freq == rrule.DAILY:
                kwargs['until'] = kwargs['dtstart'] + 10 * year # Add 25 years in occurrence table
            #self.calculatedoccurrence_set.create(event=self, start_time=start_time, end_time=end_time, **kwargs)

        occurrences = [Occurrence(event=self, start_time=occurrence, end_time=end_time, notes=None, all_day=all_day, multi_day=False) for occurrence in rrule.rrule(freq, **kwargs)]
        self.occurrence_set.bulk_create(occurrences)

    def get_occurrences(self, duration, **kwargs):
        occurrence_type = kwargs.pop('type', None)
        if occurrence_type == 'recurring':
            '''get recurring only'''
            return 'recurring'
        elif occurrence_type == 'simple':
            '''get simple occurrences only'''
            return 'simple'
        else:
            return 'all'


class Occurrence(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    notes = models.CharField(blank=True, null=True, max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    all_day = models.BooleanField()
    multi_day = models.BooleanField()

    @property
    def duration(self):
        duration = self.end_time - self.start_time

    #def get_duration(self): # return min as float
    #    return duration_calc(self.start_time, self.end_time)

    #def get_duration_hm(self): #return h:m
    #    return duration_calc(self.start_time, self.end_time, humanized=True)

    #def set_all_day_times(self, start_time):
    #    if self.all_day == True:
    #        start_time = datetime.combine(start_time, datetime.min.time())
    #        end_time = datetime.combine(start_time, datetime.max.time())
    #        return start_time, end_time

'''
rrule parameters from documentation:
freq    must be one of YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, or SECONDLY.
cache   If given, it must be a boolean value specifying to enable or disable caching of results. If you will use the same rrule instance multiple times, enabling caching will improve the performance considerably.
dtstart The recurrence start. Besides being the base for the recurrence, missing parameters in the final recurrence instances will also be extracted from this date. If not given, datetime.now() will be used instead.
interval The interval between each freq iteration. For example, when using YEARLY, an interval of 2 means once every two years, but with HOURLY, it means once every two hours. The default interval is 1.
wkst The week start day. Must be one of the MO, TU, WE constants, or an integer, specifying the first day of the week. This will affect recurrences based on weekly periods. The default week start is got from calendar.firstweekday(), and may be modified by calendar.setfirstweekday().
wount How many occurrences will be generated.
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
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
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
