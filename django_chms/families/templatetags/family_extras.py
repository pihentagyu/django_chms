from datetime import date
from django import template
from django.utils.safestring import mark_safe
import markdown2


from families.models import Family

register = template.Library()

@register.simple_tag
def newest_family():
    '''Gets the newest family that was added to the library'''
    return Family.objects.latest('created_at')

@register.inclusion_tag('families/family_nav.html')
def nav_family_list():
    '''Returns dictionary of families for navigation pane'''
    families = Family.objects.values('id', 'family_name')[:5]
    return {'families': families}

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.filter('age_calc')
def age_calc(birth_date):
    '''Get age from date of birth'''
    if birth_date:
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    '''Converts markdown text to HTML'''
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)

