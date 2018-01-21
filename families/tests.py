from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

# Create your tests here.

from .models import Family, Member, Adult, Child
from cities_local.models import Country, Region, City

class FamilyModelTests(TestCase):
    def setUp(self):
        self.country = Country(
                name = 'United States')
        self.country.save()
        self.region = Region(
                name = 'New York',
                country = self.country)
        self.region.save()

        self.city = City.objects.create(
                country = self.country,
                region = self.region,
                name = 'New York')
        self.city.save()

        self.family = Family.objects.create(
                family_name = 'Jenkins',
                address1 = '2042 Farnum Road',
                city = self.city,
                region = self.region,
                country = self.country,
                postal_code = '10013',
                )
        self.family.save()
        self.member = Member.objects.create(
                family = self.family,
                first_name = 'John',
                gender = 'M',
                birth_date = '1950-12-31'
                )
        self.member.save()
    def test_family_creation(self):
        now = timezone.now()
        self.assertLess(self.family.created_at, now)
    def test_member_creation(self):
        self.assertIn(self.member, self.family.member_set.all())

class FamilyViewsTests(TestCase):
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
        self.family2 = Family.objects.create(
                family_name = 'Matzko',
                address1 = '1945 Main Street',
                city = self.city,
                region = self.region,
                country = self.country,
                postal_code = '37505',
                )
        self.family2.save()
        self.adult = Adult.objects.create(
                family = self.family,
                first_name = 'James',
                last_name = 'Doepp',
                gender = 'M',
                )
        self.adult.save()
        self.child = Child.objects.create(
                family = self.family,
                first_name = 'Alexander',
                last_name = 'Doepp',
                gender = 'M',
                )
        self.child.save()
    def test_family_list_view(self):
        resp = self.client.get(reverse('families:family_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.family, resp.context['families'])
        self.assertIn(self.family2, resp.context['families'])
        self.assertTemplateUsed(resp, 'families/family_list.html')
        self.assertContains(resp, self.family.family_name)

    def test_family_detail_view(self):
        resp = self.client.get(reverse('families:family_detail', kwargs={'pk':
            self.family.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.family, resp.context['family'])
        self.assertTemplateUsed(resp, 'families/family_detail.html')
        self.assertContains(resp, self.family.family_name)
    
    def test_adult_detail_view(self):
        resp = self.client.get(reverse('families:member_detail', kwargs={
            'family_pk': self.family.pk,
            'member_pk': self.adult.pk,
            }))
        self.assertEqual(resp.status_code, 200) self.assertEqual(self.adult, resp.context['member']) self.assertTemplateUsed(resp, 'families/member_detail.html') self.assertContains(resp, self.adult.last_name) def test_child_detail_view(self): resp = self.client.get(reverse('families:member_detail', kwargs={ 'family_pk': self.family.pk, 'member_pk': self.child.pk })) self.assertEqual(resp.status_code, 200) self.assertEqual(self.child, resp.context['member'])
        self.assertTemplateUsed(resp, 'families/member_detail.html')
        self.assertContains(resp, self.child.last_name)



Curious what John means? Click here to find out!

Mother's maiden name
    Howlett

SSN
    134-34-8245
    You should click here to find out if your SSN is online.

Geo coordinates
    40.769538, -73.996658

Phone

Phone
    

Country code
    1

Birthday

Birthday
    

Age
    212-334-7551

Tropical zodiac
    Virgo

Online

Email Address
    JohnEJenkins@rhyta.com
    This is a real email address. Click here to activate it!

Username
    Glit1950

Password
    oob0Zeinae

Website
    caemail.com

Browser user agent
    Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Finance

MasterCard
    5179 1429 2198 9327

Expires
    3/2022

CVC2
    976

Employment

Company
    E.J. Korvette

Occupation
    Director

Physical characteristics

Height
    5' 10" (177 centimeters)

Weight
    189.9 pounds (86.3 kilograms)

Blood type
    A+

Tracking numbers

UPS tracking number
    1Z 404 719 14 4961 878 7

Western Union MTCN
    8626212282

MoneyGram MTCN
    01997816

Other

Favorite color
    Green

Vehicle
    2011 BMW 328

GUID
    5365232b-d536-4f0d-a1e3-24d601e48259

QR Code
    Click to view the QR code for this identity


