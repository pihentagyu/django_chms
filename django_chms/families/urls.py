from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.family_list, name='list'),
        url(r'(?P<family_pk>\d+)/(?P<member_type>a|d)_(?P<member_pk>\d+)/$', views.member_detail, name='member'),
        url(r'(?P<family_pk>\d+)/create_member_(?P<member_type>a|d)/$', views.member_form, name='create_member'),
        url(r'(?P<family_pk>\d+)/edit_member_(?P<member_pk>\d+)_(?P<member_type>a|d)/$', views.member_form, name='edit_member'),
        url(r'edit_family_(?P<pk>\d+)/$', views.family_edit, name='edit_family'),
        url(r'search/$', views.search, name='search'), 
        url(r'(?P<pk>\d+)/$', views.family_detail, name='detail'),
        ]
