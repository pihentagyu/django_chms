from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

# Create your tests here.

from models import Family, Member, Adult, Child

class FamilyModelTests(TestCase):
    def setUp(self):
        self.family = Family.objects.create(
                family_name = 'Doepp',
                address1 = '945 Polo Place',
                city = 'Chattanooga',
                state = 'TN',
                postal_code = '37405',
                )
        self.member = Member.objects.create(
                family = self.family,
                first_name = 'James',
                last_name = 'Doepp',
                gender = 'M',
                )

    def test_family_creation(self):
        now = timezone.now()
        self.assertLess(self.family.created_at, now)
    def test_member_creation(self):
        self.assertIn(self.member, self.family.member_set.all())

class FamilyViewsTests(TestCase):
    def setUp(self):
        self.family = Family.objects.create(
                family_name = 'Doepp',
                address1 = '945 Polo Place',
                city = 'Chattanooga',
                state = 'TN',
                postal_code = '37405',
                )
        self.family2 = Family.objects.create(
                family_name = 'Matzko',
                address1 = '1945 Main Street',
                city = 'Chattanooga',
                state = 'TN',
                postal_code = '37505',
                )
        self.member = Member.objects.create(
                family = self.family,
                first_name = 'James',
                last_name = 'Doepp',
                gender = 'M',
                )
    def test_family_list_view(self):
        resp = self.client.get(reverse('families:family_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.family, resp.context['families'])
        self.assertIn(self.family2, resp.context['families'])
        self.assertTemplateUsed(resp, 'families/family_list.html')
        self.assertContains(resp, self.family.family_name)

    def test_family_detail_view(self):
        resp = self.client.get(reverse('families:detail', kwargs={'pk':
            self.family.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.family, resp.context['family'])
        self.assertTemplateUsed(resp, 'families/family_detail.html')
        self.assertContains(resp, self.family.family_name)
    
    def test_member_detail_view(self):
        resp = self.client.get(reverse('families:member', kwargs={
            'family_pk': self.family.pk,
            'member_pk': self.member.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.member, resp.context['member'])
        self.assertTemplateUsed(resp, 'families/member_detail.html')
        self.assertContains(resp, self.member.last_name)


