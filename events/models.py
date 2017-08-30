from datetime import date, datetime
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


class SimpleEvent(Event):
    '''Event with a begin time and end time not associated with a group'''
    pass

class SimpleGroupEvent(Event):
    '''Event with a begin time and end time with one group'''
    group = models.ForeignKey(Group)


class AllDayEvent(Event):
    date = models.DateField()

    def get_begin_time(self):
        return datetime.combine(date, datetime.min.time())

    def get_end_time(self):
        return datetime.combine(date, datetime.max.time())

