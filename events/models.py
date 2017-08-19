from django.db import models

# Create your models here.

class Event(models.Model):
    EVENT_TYPES = ('simple', 'recurring',)

    class Meta:
        abstract = True
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = 


