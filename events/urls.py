from django.urls import re_path

from . import views

urlpatterns = [
        re_path(r'^$', views.EventListView.as_view(), name='event_list'),
        re_path(r'create_event/(?P<date>\d{4}-\d{2}-\d{2})/$', views.EventCreateView.as_view(), name='event_create'),
        re_path(r'create_event/(?P<start_time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})/$', views.EventCreateView.as_view(), name='event_create'),
        re_path(r'create_event/$', views.EventCreateView.as_view(), name='event_create'),
        #re_path(r'(?P<year>\d{4})-(?P<month>(0[1-9])|(1[0-2]))-(?P<day>(0[1-9])|([12][0-9])|(3[01]))/$', views.EventDailyListView.as_view(), name='event_daily'),
        #re_path(r'(?P<year>\d{4})-(?P<week>(0[1-9])|([1-4][0-9])(5[0-2]))w/$', views.EventWeeklyListView.as_view(), name='event_weekly'),
        re_path(r'(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])/$', views.EventMonthlyListView.as_view(), name='event_monthly'),
        #re_path(r'(?P<year>\d{4})/$', views.EventYearlyListView.as_view(), name='event_yearly'),
        re_path(r'delete_event_(?P<pk>\d+)/$', views.EventDeleteView.as_view(), name='event_delete'),
        re_path(r'edit_event_(?P<pk>\d+)/$', views.EventUpdateView.as_view(), name='event_edit'),
        re_path(r'(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event_detail'),
        ]
