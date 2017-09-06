##### Much of this code was taken from https://djangosnippets.org/snippets/2464/
##### Here is the template tag code. It goes in a file named 
# "event_tags.py" in a subdirectory of your app called "templatetags".
#####

import calendar
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from datetime import date, datetime, timedelta
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_monthly_calendar(parser, token):
    """
    The template tag's syntax is {% monthly_calendar year month event_list %}
    """

    try:
        tag_name, year, month, event_list = token.split_contents()
    except ValueError:
        try:
            tag_name, year, month = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    return EventCalendarNode('monthly', year, month=month)

def do_daily_calendar(parser, token):
    """
    The template tag's syntax is {% monthly_calendar year month event_list %}
    """

    try:
        tag_name, year, month, day, from_time, to_time, delta, event_list = token.split_contents()
    except ValueError:
        try:
            tag_name, year, month, day, from_time, to_time, delta = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError("%r tag requires six arguments" % token.contents.split()[0])
    return EventCalendarNode('daily', year, month=month, day=day, from_time=from_time, to_time=to_time, delta=delta)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, cal_type, year, **kwargs):# month=None, day=None, week=None, event_list=None):
        try:
            self.year = template.Variable(year)
            month = kwargs.get('month')
            day = kwargs.get('day')
            from_time = kwargs.get('from_time')
            to_time = kwargs.get('to_time')
            delta = kwargs.get('delta')
            week = kwargs.get('week')
            event_list = kwargs.get('event_list')
            self.cal_type = cal_type
            if month:
                self.month = template.Variable(month)
            if day:
                self.day = template.Variable(day)
            if from_time:
                self.from_time = template.Variable(from_time)
            if to_time:
                self.to_time = template.Variable(to_time)
            if delta:
                self.delta = template.Variable(delta)
            if week:
                self.week = template.Variable(week)
            if event_list:
                self.event_list = template.Variable(event_list)
            else:
                self.event_list = None
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        # Get the variables from the context so the method is thread-safe.
        calyear = self.year.resolve(context)
        try:
            try:
                calyear = int(calyear)
            except ValueError:
                return
            if self.cal_type in ('monthly, weekly, daily'):
                calmonth = self.month.resolve(context)
                try:
                    calmonth = int(calmonth)
                except ValueError:
                    return
            else:
                calmonth = None
            if self.cal_type == 'daily':
                calday = self.day.resolve(context)
                try:
                    calday = int(calday)
                except ValueError:
                    return
                from_time = self.from_time.resolve(context)
                to_time = self.to_time.resolve(context)
                delta = self.delta.resolve(context)
            else:
                calday = None
                from_time = None
                to_time = None
                delta = None
            if self.cal_type == 'weekly':
                calweek = self.month.resolve(context)
                try:
                    calweek = int(calweek)
                except ValueError:
                    return
            else:
                calweek = None
            if self.event_list:
                my_event_list = self.event_list.resolve(context)
                cal = EventCalendar(self.cal_type, calyear, month=calmonth, day=calday, 
                        from_time=from_time, to_time=to_time, delta=delta, week=calweek, 
                        event_list=my_event_list)
            else:
                cal = EventCalendar(self.cal_type, calyear, month=calmonth, day=calday, 
                        from_time=from_time, to_time=to_time, delta=delta, week=calweek)
            if self.cal_type == 'monthly':
                return cal.format_month()
            elif self.cal_type == 'daily':
                return cal.format_day()
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return
'''

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
'''
class EventCalendar:
    def __init__(self, cal_type, year, **kwargs):
        self.year = year
        self.month = kwargs.get('month')
        self.day = kwargs.get('day')
        self.from_time = kwargs.get('from_time')
        self.to_time = kwargs.get('to_time')
        self.delta = kwargs.get('delta')
        self.week = kwargs.get('week')
        self.event_list = kwargs.get('event_list')

    def format_month(self, event_list=None):
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
                body.append('<td class="cal"><a href="{}">{}</a></td>'.format(reverse('events:event_daily', kwargs={'day':str(day.day).zfill(2), 'month':str(self.month).zfill(2), 'year':self.year}), day.day))
        #return reverse_lazy('families:family_detail', kwargs={'pk': self.kwargs['family_pk']})
            body.append('</tr>')
        body.append('</table>')
        body.append('</div>')
        html_body = ''.join(body)
        return html_body

    def format_day(self, event_list=None):
        cal_date = date(self.year, self.month, self.day)
        cal = calendar.HTMLCalendar()
        weekday = calendar.day_name[cal_date.weekday()]
        '''Create an empty calendar table as a base'''
        body = ['<div class="cal">', '<header class="cal">', 
                '<button class="cal">«</button>', '<h2 class="cal">', 
                cal_date.strftime(settings.LONG_DATE_FORMAT), '</h2>', 
                '<button class="cal">»</button>', '</header>', '<table class="fam_list">']
        body.append('<tr class="thead">')
        body.append('<th class="cal">Events</th>')
        body.append('</tr>')
        for time in self.time_iterator(self.year, self.month, self.day, self.from_time, self.to_time, self.delta):
            body.append('<tr>')
            body.append('<td>{}</td>'.format(time.strftime(settings.TIME_FORMAT)))
            body.append('</tr>')
        body.append('</table>')
        body.append('</div>')
        html_body = ''.join(body)
        return html_body


    def time_iterator(self, year, month, day, from_time='8:00', to_time='21:00', delta=30):
        delta = timedelta(minutes=delta)
        from_hour, from_minute = from_time.split(':')
        to_hour, to_minute = to_time.split(':')
        from_time = datetime(year, month, day, int(from_hour), int(from_minute))
        to_time = datetime(year, month, day, int(to_hour), int(to_minute))
        while to_time is None or from_time <= to_time:
        	yield from_time
        	from_time = from_time + delta
        return
    
'''
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

'''

register.tag("monthly_calendar", do_monthly_calendar)
register.tag("daily_calendar", do_daily_calendar)

# Register the template tag so it is available to templates

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



