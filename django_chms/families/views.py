from itertools import chain

from braces.views import PrefetchRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from . import forms
from . import models

# Create your views here.

class FamilyCreateView(LoginRequiredMixin, CreateView):
    fields = ('user', 'family_name', 'address1', 'address2', 'city', 'postal_code', 'state', 'country', 'notes')
    model = models.Family

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        return initial


class FamilyListView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('adult_set', 'child_set')
    model = models.Family
    context_object_name = 'families'

    def get_context_data(self):
        context = super().get_context_data()
        context['email'] = 'jdoepp@gmail.com'
        return context


class FamilyDetailView(PrefetchRelatedMixin, DetailView):
    prefetch_related = ('adult_set', 'child_set')
    model = models.Family
    template_name = 'families/family_detail.html'


class FamilyDeleteView(DeleteView):
    model = models.Family
    success_url = reverse_lazy('families:list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()

class MemberDetailView(DetailView, SingleObjectMixin):
    context_object_name = 'member'
    template_name = 'families/member_detail.html'
    pk_url_kwarg = 'member_pk'

    def get_queryset(self):
        if self.kwargs['member_type'] == 'a':
            return models.Adult.objects.select_related('family').filter(family_id=self.kwargs['family_pk'])
        else:
            return models.Child.objects.select_related('family').filter(family_id=self.kwargs['family_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_type'] = self.kwargs['member_type']
        return context


class FamilySearchView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('adult_set', 'child_set')
    template_name = 'families/family_list.html'
    model = models.Family
    context_object_name = 'families'

    def get_queryset(self):
        term = self.request.GET.get('q')
        return self.model.objects.filter(Q(family_name__icontains=term)|Q(adult__first_name__icontains=term)|Q(child__first_name__icontains=term)).distinct()

    def get_context_data(self):
        context = super().get_context_data()
        context['email'] = 'jdoepp@gmail.com'
        return context


class AdultCreateView(LoginRequiredMixin, CreateView):

    model = models.Adult
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address','notes')
    template_name = 'families/member_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'a'
        return context


class ChildCreateView(LoginRequiredMixin, CreateView):

    model = models.Child
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'date_joined', 'school','notes')
    template_name = 'families/member_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        initial['last_name'] = self.model.objects.get(pk=self.kwargs['family_pk']).family.family_name
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'd'
        return context

@login_required
def member_create(request, family_pk, member_type):
    family = get_object_or_404(models.Family, pk=family_pk)
    if member_type == 'a':
        form_class = forms.AdultMemberForm
    else:
        form_class = forms.ChildMemberForm

    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.family = family
            member.save()
            messages.success(request, "Family Member added!")
            return HttpResponseRedirect(reverse('families:detail', kwargs={'pk':family_pk}))

    return render(request, 'families/member_form.html', {'form': form, 'family':family})

@login_required
def member_form(request, member_type, family_pk, member_pk=None):
    family = get_object_or_404(models.Family, pk=family_pk)
    if member_type == 'a':
        if member_pk:
            member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
        form_class = forms.AdultMemberForm
    else:
        formset = forms.ChildMemberFormset(queryset=family.child_set.all())

    if member_type == 'a':
        if member_pk:
            form = form_class(instance=member)
        else:
            form = form_class()

    if request.method == 'POST':
        if member_type == 'a':
            if member_pk:
                form = form_class(instance=member, data=request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Updated {}".format(form.cleaned_data['first_name']))
                    return HttpResponseRedirect(member.get_absolute_url())
            else:
                form = form_class(request.POST)
                if form.is_valid():
                    member = form.save(commit=False)
                    member.family = family
                    member.save()
                    messages.success(request, "Family Member added!")
                    return HttpResponseRedirect(reverse('families:detail', kwargs={'pk':family_pk}))
        else:
            formset = forms.ChildMemberFormset(request.POST, queryset=family.child_set.all())
            if formset.is_valid():
                members = formset.save(commit=False)
                for member in members:
                    member.family = family
                    member.save()
                    messages.success(request, "Added members!")
                    return HttpResponseRedirect(member.get_absolute_url())



    if member_type == 'a':
        if member_pk:
            return render(request, 'families/member_form.html', {'form': form, 'family':member.family, 'member_type':member_type})
        else:
            return render(request, 'families/member_form.html', {'form': form, 'family':family, 'member_type':member_type})
    else:
            return render(request, 'families/member_form.html', {'formset': formset, 'family':family, 'member_type':member_type})

@login_required
def family_edit(request, pk):
    family = get_object_or_404(models.Family, pk=pk)
    form = forms.FamilyForm(instance=family)
    member_forms = forms.FamilyMemberInlineFormset(queryset=form.instance.adult_set.all())
    if request.method == 'POST':
        form = forms.FamilyForm(instance=family, data=request.POST)
        member_forms = forms.FamilyMemberInlineFormset(request.POST, queryset=form.instance.adult_set.all())
        if form.is_valid() and member_forms.is_valid():
            form.save()
            members = member_forms.save(commit=False)
            for member in members:
                member.family = family
                member.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['family_name']))
        return HttpResponseRedirect(reverse('families:detail', kwargs={'pk':pk}))
    return render(request, 'families/family_form.html', {'form': form,
        'family':pk, 'formset': member_forms})

@login_required
def member_edit(request, family_pk, member_pk, member_type):
    if member_type == 'a':
        member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
        form_class = forms.AdultMemberForm
    else:
        member = get_object_or_404(models.Child, family_id=family_pk, pk=member_pk)
        form_class = forms.ChildMemberForm
    form = form_class(instance=member)

    if request.method == 'POST':
        form = form_class(instance=member, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['first_name']))
        return HttpResponseRedirect(member.get_absolute_url())
    return render(request, 'families/member_form.html', {'form': form, 'family':member.family})


