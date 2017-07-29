from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^profile/$', views.profile_view, name='profile'),
        url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
        url(r'signup/$', views.SignUpView.as_view(), name="signup"),
        ]
