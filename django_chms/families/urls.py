from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.family_list),
        url(r'(?P<family_pk>\d+)/(?P<member_pk>\d+)$', views.member_detail),
        url(r'(?P<pk>\d+)/$', views.family_detail),
         ]
