from datetime import date, datetime
from django.core.urlresolvers import reverse
from django.db import models

from families.models import Member
from groups.models import Group

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=35)
    building = models.CharField(max_length=35)
    description = models.CharField(blank=True, null=True, max_length=255)

class Event(models.Model):
    name = models.CharField(max_length=35)
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
