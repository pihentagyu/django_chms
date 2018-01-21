from braces.views import PrefetchRelatedMixin
from dal import autocomplete
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from itertools import chain
from model_utils.managers import InheritanceManagerMixin
from model_utils.managers import InheritanceQuerySet
import os
from subprocess import Popen, PIPE
import tempfile
from . import forms
from . import models
from cities_local.models import Country, Region, City
# Create your views here.

class FamilyListView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('member_set',)
    #self.model.objects.prefetch_related(Prefetch('member_set', queryset=models.Member.objects.select_subclasses(), to_attr='members'))
    model = models.Family
    context_object_name = 'families'
    ordering = ['family_name']
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        #return super(FamilyListView, self).get_queryset(request).select_subclasses()
        return InheritanceQuerySet(self.model).select_subclasses()

def family_list_as_pdf(request):
    families = models.Family.objects.all()
    families_member_related = families.prefetch_related('families_member_related')

    template = get_template('families/addressbook.tex')
    rendered_tpl = template.render({'families':families, 'member_set': families_member_related, 'media_root': settings.MEDIA_ROOT, 'church_name': settings.CHURCH_NAME}).encode('utf-8')
    # Python3 only. For python2 check out the docs!
    with tempfile.TemporaryDirectory() as tempdir:  
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            out, err = process.communicate(rendered_tpl)
            print(out, err)
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')  
    r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    r.write(pdf)
    return r

class FamilyDetailView(PrefetchRelatedMixin, DetailView):
    context_object_name = 'family'
    prefetch_related = ('member_set',)
    model = models.Family
    template_name = 'families/family_detail.html'


    #def get_context_data(self, **kwargs):
    #    context = super(FamilyDetailView, self).get_context_data(**kwargs)
    #    #context['children'] = [member for member in prefetch_related['member_set'] if member.child == True]
    #    #context['adults'] = [member for member in prefetch_related['member_set'] if member.child == False]
    #    return context



class FamilyCreateView(LoginRequiredMixin, CreateView):
    #fields = ('user', 'family_name', 'address1', 'address2', 'city', 'postal_code', 'region', 'country', 'notes')
    template_name = 'families/family_form.html'
    form_class = forms.FamilyForm
    success_url = reverse_lazy('families:family_list')
    #class Meta:
    #    model = models.Family

    #form_class =  modelform_factory(models.Family,
    #    fields = ('user', 'family_name', 'address1', 'address2', 'postal_code', 'country', 'region', 'city', 'notes'),
    #    widgets = {'country': autocomplete.ModelSelect2(url='cities_local:country_autocomplete'),
    #        'region': autocomplete.ModelSelect2(url='cities_local:region_autocomplete', forward=['country']),
    #        'city': autocomplete.ModelSelect2(url='cities_local:city_autocomplete', forward=['country', 'region']),
    #        }
    #    )

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        initial['country'] = Country.objects.get(name=settings.DEFAULT_COUNTRY).pk
        initial['region'] = Region.objects.get(name=settings.DEFAULT_REGION).pk
        initial['city'] = City.objects.get(name=settings.DEFAULT_CITY).pk
        return initial


class FamilyDeleteView(DeleteView):
    model = models.Family
    success_url = reverse_lazy('families:family_list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()


class FamilyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Family
    #fields = ('user', 'family_name', 'address1', 'address2', 'postal_code', 'country', 'region', 'city', 'notes'),
    form_class = forms.FamilyForm

class FamilySearchView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('member_set',)
    ordering = ['family_name']
    template_name = 'families/family_list.html'
    model = models.Family
    context_object_name = 'families'

    def get_queryset(self):
        term = self.request.GET.get('q')
        return self.model.objects.filter(Q(family_name__icontains=term)|Q(member__first_name__icontains=term)).distinct()


class MemberListView(ListView):
    model = models.Member
    #members = model.objects.all().select_subclasses()
    context_object_name = 'members'
    ordering = ['last_name']
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['church_name'] = settings.CHURCH_NAME
        return context


class MemberDetailView(DetailView, SingleObjectMixin):
    model = models.Member
    context_object_name = 'member'
    template_name = 'families/member_detail.html'
    pk_url_kwarg = 'member_pk'

    def get_queryset(self):
        return models.Member.objects.select_related('family').filter(family_id=self.kwargs['family_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.model.objects.get(pk=self.kwargs['member_pk'])
        context['member_pk'] = self.kwargs['member_pk']
        context['family_pk'] = self.kwargs['family_pk']
        context['age'] = member.age()
        return context


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = models.Member
    fields = ('title', 'first_name', 'last_name', 'suffix', 'fam_member_type', 'gender', 'birth_date', 
            'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address', 'school', 'notes')
    template_name = 'families/member_form.html'

    def get_success_url(self):
        return reverse_lazy('families:family_detail', kwargs={'pk': self.kwargs['family_pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        initial['last_name'] = models.Family.objects.get(pk=self.kwargs['family_pk']).family_name
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context['family_pk'] = self.kwargs['family_pk']
        return context

    def form_valid(self, form):
        form.instance.family_id = self.kwargs['family_pk']
        return super(MemberCreateView, self).form_valid(form)

class MemberDeleteView(DeleteView):
    model = models.Member
    def get_success_url(self):
        return reverse_lazy('families:family_detail', kwargs={'pk': self.kwargs['family_pk']})

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'families/member_form.html' 
    model = models.Member
    fields = ('title', 'first_name', 'last_name', 'suffix', 'fam_member_type', 'gender', 'birth_date', 'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address', 'school', 'notes')
    pk_url_kwarg = 'member_pk'

    def get_success_url(self):
        return reverse_lazy('families:member_detail', kwargs={'family_pk': self.kwargs['family_pk'], 'member_pk': self.kwargs['member_pk'] })

    def get_context_data(self):
        context = super().get_context_data()
        context['family_pk'] = self.kwargs['family_pk']
        return context
