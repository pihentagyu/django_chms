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
        self.family2 = Family.objects.create(
                family_name = 'Singh',
                address1 = '87 Shady Pines Drive',
                city = self.city,
                region = self.region,
                country = self.country,
                postal_code = '24251',
                )
        self.family2.save()
        self.adult = Adult.objects.create(
                family = self.family,
                first_name = 'Robert',
                gender = 'M',
                )
        self.adult.save()
        self.child = Child.objects.create(
                family = self.family,
                first_name = 'Jonathan',
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
        self.assertEqual(resp.status_code, 200) 
        self.assertEqual(self.adult, resp.context['member']) 
        self.assertTemplateUsed(resp, 'families/member_detail.html') 
        self.assertContains(resp, self.adult.last_name) 
        
    def test_child_detail_view(self): 
        resp = self.client.get(reverse('families:member_detail', kwargs={ 'family_pk': self.family.pk,
            'member_pk': self.child.pk })) self.assertEqual(resp.status_code, 200) 
        self.assertEqual(self.child, resp.context['member'])
        self.assertTemplateUsed(resp, 'families/member_detail.html')
        self.assertContains(resp, self.child.last_name)

