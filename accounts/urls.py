from django.urls import re_path

from . import views

urlpatterns = [
        re_path(r'^profile/$', views.profile_view, name='profile'),
        re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
        re_path(r'^login/$', views.LoginView.as_view(), name='login'),
        re_path(r'signup/$', views.SignUpView.as_view(), name="signup"),
        ]
