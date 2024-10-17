"""django_chms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
#Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from . import views

urlpatterns = [
    re_path(r'^$', views.front_page, name='home'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^families/', include(('families.urls', 'families'), namespace='families')),
    re_path(r'^cities_local/', include(('cities_local.urls', 'cities_local'), namespace='cities_local')),
    re_path(r'^groups/', include(('groups.urls', 'groups'), namespace='groups')),
    re_path(r'^events/', include(('events.urls', 'events'), namespace='events')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
            re_path(r'^__debug__/', include(debug_toolbar.urls))
            ]
