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

@register.filter('time_estimate')
def time_estimate(word_count):
    '''Estimate the time it takes based on word count'''
    minutes = round(word_count/20)
    return minutes

@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    '''Converts markdown text to HTML'''
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)

