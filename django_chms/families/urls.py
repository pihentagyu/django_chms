from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.family_list, name='list'),
        url(r'(?P<family_pk>\d+)/a(?P<member_pk>\d+)$', 
            views.adult_detail, name='adult'),
        url(r'(?P<family_pk>\d+)/d(?P<member_pk>\d+)$', 
            views.dependent_detail, name='dependent'),
        url(r'(?P<family_pk>\d+)/create_adult_member/$',
            views.adult_member_create, name='create_adult_member'),
        url(r'(?P<family_pk>\d+)/edit_adult_member(?P<member_pk>\d+)$', 
            views.adult_member_edit, name='edit_adult_member'),
        url(r'(?P<pk>\d+)/$', views.family_detail, name='detail'),
         ]
