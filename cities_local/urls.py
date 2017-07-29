from cities_local.views import CountryAutocomplete, RegionAutocomplete, CityAutocomplete
from django.conf.urls import url

from . import views

urlpatterns = [
    url( r'^country_autocomplete/$', CountryAutocomplete.as_view(), name='country_autocomplete'),
    url( r'^region_autocomplete/$', RegionAutocomplete.as_view(), name='region_autocomplete'),
    url( r'^city_autocomplete/$', CityAutocomplete.as_view(), name='city_autocomplete'),
        ]
