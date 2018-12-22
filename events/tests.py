from datetime import date, time, datetime, timedelta
from django.test import TestCase
import pytz

from .models import Location, Event, Occurrence

from cities_local.models import Country, Region, City
from families.models import Family, Member
from groups.models import Group, GroupType, GroupMember
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
        self.member = Member.objects.create(
                family = self.family,
                first_name = 'James',
                last_name = 'Doepp',
                gender = 'M',
                )
        self.member.save()

        self.group_type = GroupType.objects.create(
            group_type = 'Sunday School'
            )
        self.group_type.save()

        self.group = Group.objects.create(
            group_name = 'Kid\'s Praise',
            group_type = self.group_type,
            group_description = '',
        )
        self.group.save()

        self.group_member = GroupMember.objects.create(
                member = self.member,
                group = self.group
                )
        self.group_member.save()

        self.location = Location.objects.create(
                name = 'Room 101',
                building = 'Main building',
                description = 'No description necessary'
                )
        self.location.save()


    def test_get_absolute_url(self):
        self.event = Event.objects.create(
                name = 'Kid\'s Praise',
                event_type = 'S',
                description = 'Children\'s Sunday school',
                creator = self.member,
                group = self.group,
                location = self.location 
                )
        self.event.save()
        url = self.event.get_absolute_url()
        print(url)

    def test_add_occurences(self):
        self.event = Event.objects.create(
                name = 'Kid\'s Praise',
                event_type = 'M',
                description = 'Children\'s Sunday school',
                creator = self.member,
                group = self.group,
                location = self.location 
                )
        self.event.save()
        
        tzinfo = pytz.utc
        dtstart = datetime(2018,11,24,12,30,0,0, tzinfo)
        until = datetime(2018,12,24,12,30,0,0, tzinfo)
        freq = 1
        duration = timedelta(hours=1, minutes=15)

        self.event.add_occurrences(duration, dtstart=dtstart, until=until)
        print(self.event.occurrence_set)
        occurrences = Occurrence.objects.filter(event=self.event)

        for occurence in occurrences:
            print(occurence.start_time, occurence.duration)


class OccurrenceModelTests(TestCase):
    pass
