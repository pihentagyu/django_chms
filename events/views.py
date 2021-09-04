from braces.views import PrefetchRelatedMixin
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Prefetch, Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSetView

from . import forms
from . import models

# Create your views here.

class EventListView(PrefetchRelatedMixin, ListView):
    model = models.Occurrence
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    #ordering = ['start_time',]


    def get_context_data(self):
        context = super().get_context_data()
        context['church_name'] = settings.CHURCH_NAME
        return context

    def get_queryset(self):
        return self.model.objects.filter(start_time__date__gte=datetime.today()).order_by('start_time')


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
            #|(Q(end_time__year=self.kwargs['year'],
            #end_time__month=self.kwargs['month']))
            )


class EventWeeklyListView(ListView):
    model = models.Occurrence
    context_object_name = 'events'
    template_name = "events/event_list.html"

    class Meta:
        ordering = ['start_time']

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
            #|(Q(end_time__year=self.kwargs['year'],
            #end_time__month=self.kwargs['month'], 
            #end_time__day=self.kwargs['day']))
            )


class EventDetailView(DetailView, ):
    model = models.Event
    context_object_name = 'event'
    template_name = "events/event_detail.html"

class EventCreateView(LoginRequiredMixin, CreateView):
    model = models.Event
    form_class = forms.EventForm
 
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        self.start_time = self.kwargs.get('start_time', None)
        self.duration = self.kwargs.get('duration', None)
        self.date = self.kwargs.get('date', None)
        if self.start_time:
            self.start_time = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M:%S')
        elif self.date:
            self.start_time = datetime.strptime(self.date, '%Y-%m-%d')
        
        context = super(EventCreateView, self).get_context_data(**kwargs)
        if 'post_occurrences' in self.request.POST:
            #context['occurrences'] = forms.OccurrenceFormset(self.request.POST,
            #       form_kwargs={'start_time': self.start_time, 'end_time': self.end_time})
            context['occurrences'] = forms.OccurrenceFormset(self.request.POST)
            context['recurring_events'] = None
            #context['occurrences'].fields['start_time'].required = True
            #context['occurrences'].fields['end_time'].required = True
            #context['occurrences'].fields['all_day'].required = True
        elif 'post_recurring' in self.request.POST:
            context['recurring_events'] = forms.RecurringEventForm(self.request.POST)
            context['recurring_events'].fields['freq'].required = True
            context['recurring_events'].fields['start_time'].required = True
            context['recurring_events'].fields['duration'].required = True
            context['recurring_events'].fields['until'].required = True
            context['occurrences'] = None
        else:
            context['occurrences'] = forms.OccurrenceFormset(form_kwargs={'start_time': self.start_time,
                 'end_time': self.start_time + timedelta(minutes=30)})
            context['recurring_events'] = forms.RecurringEventForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        #print(context)
        occurrences = context.get('occurrences', None)
        recurring_events = context.get('recurring_events', None)
        self.object = form.save()
        with transaction.atomic():
            if occurrences != None:
                if occurrences.is_valid():
                    occurrences.instance = self.object
                    print(occurrences)
                    occurrences.save()
                    #self.object.add_occurrences(**occurrences.cleaned_data)
                else:
                    print('occurence errors:')
                    for error in occurrences.errors:
                        print(error)
            elif recurring_events != None:
                if recurring_events.is_valid():
                    #self.object = form.save()
                    print(recurring_events.cleaned_data)
                    self.object.add_occurrences(**recurring_events.cleaned_data)
                else:
                    print('recurring_events errors:')
                    for error in recurring_events.errors:
                        print(error)


            ##    #context.update({'occurrences': occurrences})

        return super(EventCreateView, self).form_valid(form)

class OccurrenceInline(InlineFormSetFactory):
    fields = ('start_time', 'duration', 'notes', 'all_day', 'multi_day')
    #max_num = 1
    model = models.Occurrence

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

