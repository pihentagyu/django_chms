from cities_local.views import CountryAutocomplete, RegionAutocomplete, CityAutocomplete
from django.urls import re_path

from . import views

urlpatterns = [
    re_path( r'^country_autocomplete/$', CountryAutocomplete.as_view(), name='country_autocomplete'),
    re_path( r'^region_autocomplete/$', RegionAutocomplete.as_view(), name='region_autocomplete'),
    re_path( r'^city_autocomplete/$', CityAutocomplete.as_view(), name='city_autocomplete'),
        ]
