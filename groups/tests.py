from django.test import TestCase

from .models import GroupType, Group, MemRole, GroupMember

# Create your tests here.

class GroupTypeTest(TestCase):
    def setUp(self):
        self.group_type = GroupType.objects.create(
                group_type = 'Sunday School'
                )


class GroupTest(TestCase):
    def setUp(self):
        self group = GroupType.objects.create(
            group_name = 'Kid\'s Praise',
            group_type = '',
            group_description = '',
            group_members = ''
        )
    
class Megroup_membmRoleTest(TestCase):
    pass


class GroupMemberTest(TestCase):
    pass
