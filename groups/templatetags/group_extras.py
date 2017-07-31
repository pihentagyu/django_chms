from django import template

from groups.models import Group

register = template.Library()


@register.filter('get_total_members')
def get_total_members(members_set_list):
    '''Returns the total of all members in the group'''
    return len(members_set_list.all())
