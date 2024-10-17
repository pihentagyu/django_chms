from django.urls import re_path

from . import views

urlpatterns = [
        re_path(r'^$', views.GroupListView.as_view(), name='group_list'),
        re_path(r'create_grouptype/$', views.GroupTypeCreateView.as_view(), name='grouptype_create'),
        re_path(r'grouptype/$', views.GroupTypeListView.as_view(), name='grouptype_list'),
        re_path(r'create_group/$', views.GroupCreateView.as_view(), name='group_create'),
        re_path(r'create_member/(?P<group_pk>\d+)$', views.MemberCreateView.as_view(), name='member_create'),
        re_path(r'delete_member_(?P<group_pk>\d+)_(?P<pk>\d+)/$', views.MemberDeleteView.as_view(), name='member_delete'),
        re_path(r'delete_group_(?P<pk>\d+)/$', views.GroupDeleteView.as_view(), name='group_delete'),
        re_path(r'edit_grouptype_(?P<pk>\d+)/$', views.GroupTypeUpdateView.as_view(), name='grouptype_edit'),
        re_path(r'edit_group_(?P<pk>\d+)/$', views.GroupUpdateView.as_view(), name='group_edit'),
        re_path(r'search/$', views.GroupSearchView.as_view(), name='group_search'), 
        re_path(r'grouptype/(?P<pk>\d+)/$', views.GroupTypeGroupListView.as_view(), name='grouptype_group_list'),
        re_path(r'(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
        ]
