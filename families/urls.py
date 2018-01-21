from django.conf.urls import url

from . import views

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
        url(r'^$', views.FamilyListView.as_view(), name='family_list'),
        url(r'^members/$', views.MemberListView.as_view(), name='member_list'),
        url(r'^addressbook$', views.family_list_as_pdf, name='addressbook'),
        url(r'(?P<family_pk>\d+)/(?P<member_pk>\d+)/$', views.MemberDetailView.as_view(), name='member_detail'),
        url(r'(?P<family_pk>\d+)/create_member/$', views.MemberCreateView.as_view(), name='member_create'),
        url(r'(?P<family_pk>\d+)/delete_member_(?P<pk>\d+)/$', views.MemberDeleteView.as_view(), name='member_delete'),
        url(r'(?P<family_pk>\d+)/edit_member_(?P<member_pk>\d+)/$', views.MemberUpdateView.as_view(), name='member_edit'),
        url(r'edit_family_(?P<pk>\d+)/$', views.FamilyUpdateView.as_view(), name='family_edit'),
        url(r'delete_family_(?P<pk>\d+)/$', views.FamilyDeleteView.as_view(), name='family_delete'),
        url(r'create_family/$', views.FamilyCreateView.as_view(), name='family_create'),
        url(r'search/$', views.FamilySearchView.as_view(), name='search'), 
        url(r'(?P<pk>\d+)/$', views.FamilyDetailView.as_view(), name='family_detail'),
        ]
