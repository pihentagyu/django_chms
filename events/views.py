from braces.views import PrefetchRelatedMixin
from datetime import datetime
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet

from . import forms
from . import models

# Create your views here.

class EventListView(PrefetchRelatedMixin, ListView):
    model = models.Occurrence
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['start_time']
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['church_name'] = settings.CHURCH_NAME
        return context

    def get_queryset(self):
        return self.model.objects.filter(start_time__date__gte=datetime.today())


class EventYearlyListView(ListView):
    model = models.Occurrence
    context_object_name = 'events'
    template_name = "events/event_year_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['year'] = self.kwargs['year']
        return context

class EventMonthlyListView(ListView):
    model = models.Occurrence
    context_object_name = 'events'
    template_name = "events/monthly_calendar.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['calyear'] = self.kwargs['year']
        context['calmonth'] = self.kwargs['month']
        return context

    def get_queryset(self):
        # Queries the events in the Occurrence table that fall on the given month
        return self.model.objects.filter(Q(start_time__year=self.kwargs['year'],
            start_time__month=self.kwargs['month'])
            |(Q(end_time__year=self.kwargs['year'],
            end_time__month=self.kwargs['month'])
            )
            )


class EventWeeklyListView(ListView):
    model = models.Occurrence
    context_object_name = 'events'
    template_name = "events/event_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['year'] = self.kwargs['year']
        context['week'] = self.kwargs['week']
        return context


class EventDailyListView(ListView):
    model = models.Occurrence
    context_object_name = 'events'
    template_name = "events/daily_events.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['calyear'] = self.kwargs['year']
        context['calmonth'] = self.kwargs['month']
        context['calday'] = self.kwargs['day']
        context['from_time'] = settings.DEFAULT_DAY_BEGIN
        context['to_time'] = settings.DEFAULT_DAY_END
        context['delta'] = settings.DEFAULT_TIME_INTERVAL
        return context

    def get_queryset(self):
        # Queries the events in the Occurrence table that fall on the given day
        ## 1. that begin on that day
        ## 2. that end on the day
        ## 3. (to do) that begin before and end after that day
        return self.model.objects.filter(Q(start_time__year=self.kwargs['year'],
            start_time__month=self.kwargs['month'], 
            start_time__day=self.kwargs['day'])
            |(Q(end_time__year=self.kwargs['year'],
            end_time__month=self.kwargs['month'], 
            end_time__day=self.kwargs['day']))
            )

class EventDetailView(DeleteView):
    model = models.Event
    context_object_name = 'event'
    template_name = "events/event_detail.html"


class OccurrenceInline(InlineFormSet):
    fields = ('start_time', 'end_time')
    max_num = 1
    model = models.Occurrence


class EventCreateView(LoginRequiredMixin, CreateView):
    model = models.Event
    form_class = forms.EventForm
 
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        self.start_time = self.kwargs.get('start_time', 'none')
        self.end_time = self.kwargs.get('end_time', 'none')
        if self.start_time:
            self.start_time = datetime.strptime(self.start_time, '%Y%m%d%H%M')
        if self.end_time:
            self.end_time = datetime.strptime(self.end_time, '%Y%m%d%H%M')
        
        if 'post_occurrences' in self.request.POST:
            context['occurrences'] = forms.OccurrenceFormset(self.request.POST,
                    form_kwargs={'start_time': self.start_time, 'end_time': self.end_time})
        elif 'post_recurrent' in self.request.POST:
            context['recurring_events'] = forms.RecurringFormset(self.request.POST)
        else:
            context['occurrences'] = forms.OccurrenceFormset(form_kwargs={'start_time': self.start_time,
                 'end_time': self.end_time})
            context['recurring_events'] = forms.RecurringFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        #print(context)
        occurrences = context['occurrences']
        recurring_events = context.get('recurring_events')
        with transaction.atomic():
            self.object = form.save()
            if occurrences.is_valid():
                #print(occurrences)
                occurrences.save()
                #self.object.add_occurrences(**occurrences.cleaned_data)
            elif recurring_events.is_valid():
                print(recurring_events.cleaned_data)
                self.object.add_occurrences(**recurring_events.cleaned_data)
            else:
                print('recurring_events errors:')
                for error in recurring_events.errors:
                    print(error)
                print('occurence errors:')
                for error in occurrences.errors:
                    print(error)


            ##    #context.update({'occurrences': occurrences})

        return super(EventCreateView, self).form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
    model = models.Event
    template_name = 'events/event_form.html'
    fields = ('name', 'location', 'group', 'description', 'creator')
    inlines = (OccurrenceInline,)


class EventDeleteView(DeleteView):
    model = models.Event
    success_url = reverse_lazy('events:event_list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()

