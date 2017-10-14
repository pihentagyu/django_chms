from datetime import date, datetime
from dateutil.rrule import *
from django.core.urlresolvers import reverse
from django.db import models

from families.models import Member
from groups.models import Group

# Create your models here.
EVENT_TYPE_CHOICES = (
        ('S', 'Simple'),
        ('M', 'Multiple Occurrence'),
        ('R', 'Recurring Event'),
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
    def add_occurrences(self, start_time, end_time, **rrule_params):
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
        count = rrule_params.get('count')
        until = rrule_params.get('until')
        if not (count or until):
            self.occurrence_set.create(start_time=start_time, end_time=end_time)
        else:
            rrule_params.setdefault('freq', rrule.DAILY)
            delta = end_time - start_time
            occurrences = []
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                occurrences.append(Occurrence(start_time=ev, end_time=ev + delta, event=self))
            self.occurrence_set.bulk_create(occurrences)


class Occurrence(models.Model):
    event = models.ForeignKey(Event)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def get_duration(self):
        from events.templatetags.event_extras import duration_calc
        return duration_calc(self.begin_time, self.end_time)


#class AllDayEvent(Event):
#    date = models.DateField()
#
#    def get_begin_time(self):
#        return datetime.combine(date, datetime.min.time())
#
#    def get_end_time(self):
#        return datetime.combine(date, datetime.max.time())
#
