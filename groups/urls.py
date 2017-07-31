from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.GroupListView.as_view(), name='group_list'),
        url(r'create_group/$', views.GroupCreateView.as_view(), name='create_group'),
        url(r'delete_group_(?P<pk>\d+)/$', views.GroupDeleteView.as_view(), name='delete_group'),
        url(r'edit_group_(?P<pk>\d+)/$', views.GroupUpdateView.as_view(), name='edit_group'),
        url(r'search/$', views.GroupSearchView.as_view(), name='search'), 
        url(r'(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
        ]
