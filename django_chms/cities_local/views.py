from django.shortcuts import render
from dal.autocomplete import Select2QuerySetView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

# Create your views here.

class CountryAutocomplete(LoginRequiredMixin, Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return models.Country.objects.none()

        qs = models.Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class RegionAutocomplete(LoginRequiredMixin, Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return models.Region.objects.none()

        qs = models.Region.objects.all()

        country = self.forwarded.get('country', None)

        if country:
            qs = qs.filter(country=country)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class CityAutocomplete(LoginRequiredMixin, Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return models.City.objects.none()

        qs = models.City.objects.all()

        region = self.forwarded.get('region', None)

        if region:
            qs = qs.filter(region=region)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

