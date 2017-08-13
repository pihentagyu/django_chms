from django.conf.urls import url

from . import views

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
        url(r'^$', views.FamilyListView.as_view(), name='family_list'),
        url(r'^members/$', views.MemberListView.as_view(), name='member_list'),
        url(r'^addressbook$', views.family_list_as_pdf, name='addressbook'),
        url(r'(?P<family_pk>\d+)/(?P<member_type>a|d)_(?P<member_pk>\d+)/$', views.MemberDetailView.as_view(), name='member_detail'),
        url(r'(?P<family_pk>\d+)/create_adult/$', views.AdultCreateView.as_view(), name='adult_create'),
        url(r'(?P<family_pk>\d+)/create_child/$', views.ChildCreateView.as_view(), name='child_create'),
        url(r'(?P<family_pk>\d+)/edit_adult_(?P<member_pk>\d+)/$', views.AdultUpdateView.as_view(), name='adult_edit'),
        url(r'(?P<family_pk>\d+)/edit_child_(?P<member_pk>\d+)/$', views.ChildUpdateView.as_view(), name='child_edit'),
        url(r'edit_family_(?P<pk>\d+)/$', views.FamilyUpdateView.as_view(), name='family_edit'),
        url(r'delete_family_(?P<pk>\d+)/$', views.FamilyDeleteView.as_view(), name='family_delete'),
        url(r'create_family/$', views.FamilyCreateView.as_view(), name='family_create'),
        url(r'search/$', views.FamilySearchView.as_view(), name='search'), 
        url(r'(?P<pk>\d+)/$', views.FamilyDetailView.as_view(), name='family_detail'),
        ]
