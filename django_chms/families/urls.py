from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.FamilyListView.as_view(), name='list'),
        url(r'(?P<family_pk>\d+)/(?P<member_type>a|d)_(?P<member_pk>\d+)/$', views.MemberDetailView.as_view(), name='member'),
        url(r'(?P<family_pk>\d+)/create_adult/$', views.AdultCreateView.as_view(), name='create_adult'),
        url(r'(?P<family_pk>\d+)/create_child/$', views.ChildCreateView.as_view(), name='create_child'),
        url(r'(?P<family_pk>\d+)/edit_member_(?P<member_pk>\d+)_(?P<member_type>a|d)/$', views.member_form, name='edit_member'),
        url(r'edit_family_(?P<pk>\d+)/$', views.family_edit, name='edit_family'),
        url(r'delete_family_(?P<pk>\d+)/$', views.FamilyDeleteView.as_view(), name='delete_family'),
        url(r'create_family/$', views.FamilyCreateView.as_view(), name='create_family'),
        url(r'search/$', views.FamilySearchView.as_view(), name='search'), 
        url(r'(?P<pk>\d+)/$', views.FamilyDetailView.as_view(), name='detail'),
        ]
