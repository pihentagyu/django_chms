##### Much of this code was taken from https://djangosnippets.org/snippets/2464/
##### Here is the template tag code. It goes in a file named 
# "event_tags.py" in a subdirectory of your app called "templatetags".
#####

import calendar
from django import template
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_empty_calendar(parser, token):
    """
    The template tag's syntax is {% event_calendar year month %}
    """

    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    return EmptyCalendarNode(year, month)

def do_event_calendar(parser, token):
    """
    The template tag's syntax is {% event_calendar year month event_list %}
    """

    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires three arguments" % token.contents.split()[0])
    return EventCalendarNode(year, month)

class EmptyCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list=None):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            if event_list:
                self.event_list = template.Variable(event_list)
            else:
                self.event_list = None
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            if self.event_list:
                my_event_list = self.event_list.resolve(context)
                cal = EventCalendar(my_event_list)
            else:
                cal = EmptyCalendar(int(my_month), int(my_year))
            return cal.format_month(int(my_month), int(my_year))
            #return cal.format_month()
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, event_list=None):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            if event_list:
                self.event_list = template.Variable(event_list)
            else:
                self.event_list = None
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            if self.event_list:
                my_event_list = self.event_list.resolve(context)
                cal = EventCalendar(my_event_list)
            else:
                cal = calendar.HTMLCalendar() 
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return


class EventCalendar(calendar.HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.`
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append(esc(event.series.primary_name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date_and_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


class EmptyCalendar:
    def __init__(self, month, year):
        self.month = month
        self.year = year
    def format_month(self, month, year):
        cal = calendar.HTMLCalendar()
        '''Create an empty calendar table as a base'''
        body = ['<div class="cal">', '<header class="cal">', '<button class="cal">«</button>', '<h2 class="cal">', calendar.month_name[self.month], ' ', str(self.year), '</h2>', '<button class="cal">»</button>', '</header>', '<table class="cal">']
        body.append('<tr class="thead">')
        for weekday in calendar.day_abbr:
            body.append('<th class="cal">{}</th>'.format(weekday))
        body.append('</tr>')
        for week in cal.monthdatescalendar(self.year, self.month):
            body.append('<tr class="cal">')
            for day in week:
                body.append('<td class="cal"><a href="{}">{}</a></td>'.format(reverse_lazy('events:event_daily', kwargs={'day':str(day.day).zfill(2), 'month':str(self.month).zfill(2), 'year':self.year}), day.day))
        #return reverse_lazy('families:family_detail', kwargs={'pk': self.kwargs['family_pk']})
            body.append('</tr>')
        body.append('</table>')
        body.append('</div>')
        html_body = ''.join(body)
        return html_body


# Register the template tag so it is available to templates
register.tag("event_calendar", do_empty_calendar)

##### Here's code for the view to look up the event objects for to put in 
# the context for the template. It goes in your app's views.py file (or 
# wherever you put your views).
#####

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

def this_month(request):
    """
    Show calendar of events this month.
    """
    today = datetime.now()
    return mycalendar(request, today.year, today.month)


def mycalendar(request, year, month, series_id=None):
    """
    Show calendar of events for a given month of a given year.
    ``series_id``
    The event series to show. None shows all event series.

    """

    my_year = int(year)
    my_month = int(month)
    my_calendar_from_month = datetime(my_year, my_month, 1)
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])

    my_events = Event.objects.filter(date_and_time__gte=my_calendar_from_month).filter(date_and_time__lte=my_calendar_to_month)
    if series_id:
        my_events = my_events.filter(series=series_id)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render_to_response("cal_template.html", { 'events_list': my_events,
                                                        'month': my_month,
                                                        'month_name': named_month(my_month),
                                                        'year': my_year,
                                                        'previous_month': my_previous_month,
                                                        'previous_month_name': named_month(my_previous_month),
                                                        'previous_year': my_previous_year,
                                                        'next_month': my_next_month,
                                                        'next_month_name': named_month(my_next_month),
                                                        'next_year': my_next_year,
                                                        'year_before_this': my_year_before_this,
                                                        'year_after_this': my_year_after_this,
    }, context_instance=RequestContext(request))



@register.simple_tag
def this_year():
    '''Returns the current year'''
    return date.today().year

@register.simple_tag
def this_month():
    '''Returns the current month'''
    return date.strftime(date.today(), '%m')



