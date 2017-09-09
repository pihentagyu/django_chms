from datetime import date, datetime
from django.core.urlresolvers import reverse
from django.db import models

from families.models import Member
from groups.models import Group

# Create your models here.

class Event(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=35)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(Member)

    def get_duration(self):
        from events.templatetags.event_extras import duration_calc
        return duration_calc(self.begin_time, self.end_time)

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={
            'pk': self.id,
            })


class SimpleEvent(Event):
    '''Event with a begin time and end time not associated with a group'''
    def __str__(self):
        return self.name

class SimpleGroupEvent(Event):
    '''Event with a begin time and end time with one group'''
    group = models.ForeignKey(Group)


class AllDayEvent(Event):
    date = models.DateField()

    def get_begin_time(self):
        return datetime.combine(date, datetime.min.time())

    def get_end_time(self):
        return datetime.combine(date, datetime.max.time())

