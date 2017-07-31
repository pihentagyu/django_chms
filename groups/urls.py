from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.GroupListView.as_view(), name='group_list'),
        url(r'create_group/$', views.GroupCreateView.as_view(), name='create_group'),
        url(r'(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
        ]
