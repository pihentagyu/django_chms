from cities_light.abstract_models import AbstractCountry, AbstractRegion, AbstractCity, AbstractSubRegion
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

#connect_default_signals(SubRegion)

class City(AbstractCity):
    pass
connect_default_signals(City)




