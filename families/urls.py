from django.urls import re_path

from . import views

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
        re_path(r'^$', views.FamilyListView.as_view(), name='family_list'),
        re_path(r'^members/$', views.MemberListView.as_view(), name='member_list'),
        re_path(r'^addressbook$', views.family_list_as_pdf, name='addressbook'),
        re_path(r'edit_family/(?P<pk>\d+)/$', views.FamilyUpdateView.as_view(), name='family_edit'),
        re_path(r'delete_family_(?P<pk>\d+)/$', views.FamilyDeleteView.as_view(), name='family_delete'),
        re_path(r'(?P<family_pk>\d+)/(?P<member_pk>\d+)/$', views.MemberDetailView.as_view(), name='member_detail'),
        re_path(r'(?P<family_pk>\d+)/create_member/$', views.MemberCreateView.as_view(), name='member_create'),
        re_path(r'(?P<family_pk>\d+)/delete_member_(?P<pk>\d+)/$', views.MemberDeleteView.as_view(), name='member_delete'),
        re_path(r'(?P<family_pk>\d+)/edit_member_(?P<member_pk>\d+)/$', views.MemberUpdateView.as_view(), name='member_edit'),
        re_path(r'create_family/$', views.FamilyCreateView.as_view(), name='family_create'),
        re_path(r'search/$', views.FamilySearchView.as_view(), name='search'), 
        re_path(r'(?P<pk>\d+)/$', views.FamilyDetailView.as_view(), name='family_detail'),
        ]
