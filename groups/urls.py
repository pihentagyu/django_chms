from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.GroupListView.as_view(), name='group_list'),
        url(r'create_grouptype/$', views.GroupTypeCreateView.as_view(), name='grouptype_create'),
        url(r'grouptype/$', views.GroupTypeListView.as_view(), name='grouptype_list'),
        url(r'create_group/$', views.GroupCreateView.as_view(), name='group_create'),
        url(r'create_member/(?P<group_pk>\d+)$', views.MemberCreateView.as_view(), name='member_create'),
        url(r'delete_member_(?P<group_pk>\d+)_(?P<pk>\d+)/$', views.MemberDeleteView.as_view(), name='member_delete'),
        url(r'delete_group_(?P<pk>\d+)/$', views.GroupDeleteView.as_view(), name='group_delete'),
        url(r'edit_grouptype_(?P<pk>\d+)/$', views.GroupTypeUpdateView.as_view(), name='grouptype_edit'),
        url(r'edit_group_(?P<pk>\d+)/$', views.GroupUpdateView.as_view(), name='group_edit'),
        url(r'search/$', views.GroupSearchView.as_view(), name='group_search'), 
        url(r'grouptype/(?P<pk>\d+)/$', views.GroupTypeGroupListView.as_view(), name='grouptype_group_list'),
        url(r'(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
        ]
