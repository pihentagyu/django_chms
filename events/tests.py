from django.test import TestCase

from .models import Location, Event, Occurrence

from cities_local.models import Country, Region, City
from families.models import Member
# Create your tests here.

class LocationModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
                name = 'Room 101',
                building = 'Main building',
                description = 'No description necessary'
                )
        self.location.save()

class EventModelTests(TestCase):
    def setUp(self):
        self.country = Country(
            name = 'United States')
        self.country.save()

        self.region = Region(
            name = 'Tennessee',
            country = self.country)
        self.region.save()

        self.city = City.objects.create(
                country = self.country,
                region = self.region,
                name = 'Chattanooga')
        self.city.save()

        self.family = Family.objects.create(
                family_name = 'Doe',
                address1 = '239 Main Street',
                city = self.city,
                region = self.region,
                country = self.country,
                postal_code = '37405',
                )
        self.family.save()
        self.adult = Adult.objects.create(
                family = self.family,
                first_name = 'James',
                last_name = 'Doepp',
                gender = 'M',
                )
        self.adult.save()
        self.event = Events.objects.create(
                name = 'Kid\'s Praise',
                event_type = 'S',
                description = 'Children\'s Sunday school',
                creator = self.adult,
                group = self.group,
                location = self.location 
                )
        self.event.save()


class OccurrenceModelTests(TestCase):
    pass
