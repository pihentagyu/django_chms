from django.test import TestCase
from django.urls import reverse

from .models import GroupType, Group, MemRole, GroupMember
from cities_local.models import Country, Region, City
from families.models import Family, Member

# Create your tests here.

class GroupTypeTest(TestCase):
    def setUp(self):
        self.group_type = GroupType.objects.create(
                group_type = 'Sunday School'
                )


class GroupTest(TestCase):
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
                birth_date = '1950-12-31',
                fam_member_type = 'a',
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
    def test_group_list_view(self):
        resp = self.client.get(reverse('groups:group_list'))
    #    self.assertEqual(resp.status_code, 200)
    #    self.assertIn(self.group, resp.context['groups'])
    #    self.assertTemplateUsed(resp, 'groups/group_list.html')
    #    self.assertContains(resp, self.group.group_name)
        print(resp)
    
class Megroup_membmRoleTest(TestCase):
    pass


class GroupMemberTest(TestCase):
    pass
