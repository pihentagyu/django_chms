from cities_light.abstract_models import AbstractCountry, AbstractRegion, AbstractSubRegion, AbstractCity 
from cities_light.receivers import connect_default_signals
from django.db import models

# Create your models here.

class Country(AbstractCountry):
    pass

connect_default_signals(Country)


class Region(AbstractRegion):
    pass
connect_default_signals(Region)

class SubRegion(AbstractSubRegion):
    pass
connect_default_signals(SubRegion)

class City(AbstractCity):
    timezone = models.CharField(max_length=40)
connect_default_signals(City)




