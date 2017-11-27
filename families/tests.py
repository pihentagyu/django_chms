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
                first_name = 'John',
                last_name = 'Doe',
                gender = 'M',
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
            'member_type': 'a'}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.adult, resp.context['member'])
        self.assertTemplateUsed(resp, 'families/member_detail.html')
        self.assertContains(resp, self.adult.last_name)

    def test_child_detail_view(self):
        resp = self.client.get(reverse('families:member_detail', kwargs={
            'family_pk': self.family.pk,
            'member_pk': self.child.pk,
            'member_type': 'd'}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.child, resp.context['member'])
        self.assertTemplateUsed(resp, 'families/member_detail.html')
        self.assertContains(resp, self.child.last_name)

