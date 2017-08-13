from datetime import date
from django import template
from django.utils.safestring import mark_safe
import markdown2
import pypandoc


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


@register.filter('markdown_to_latex')
def markdown_to_latex(markdown_text):
    '''Converts markdown text to LaTeX'''
    tex_body = pypandoc.convert_text(markdown_text, format='markdown', to='latex')
    return mark_safe(tex_body)

@register.filter('join_by')
def join_by(value, arg=', '):
    return arg.join(value)

@register.filter('set_fields_joined')
def set_fields_joined(set_name, field):
    '''Takes all members of a related set and returns all fields from those related values joined delimited by commas'''
    try:
        set_name_all = set_name.all()
        all_fields = [m.__dict__ for m in set_name_all]
        res = [f.get(field) for f in all_fields]
        return ', '.join(res)
    except AttributeError:
        print(set_name)
        return set_name

@register.filter('list_joined')
def list_joined(items, delim=", "):
    '''Joins a list with the given delimiter'''
    if item:
        item_list = [item for item in items]
        return delim.join(item_list)
    else:
        return ''

@register.filter('check_attr')
def check_attr(item, attr):
    '''Returns 'True' if hasattr''' 
    if hasattr(item, attr):
        return True
    else:
        return False

@register.filter('get_subclass')
def get_subclass(related_set, subclass):
    return [member for member in related_set if hasattr(member, subclass)]
