from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import forms
from . import models

# Create your views here.

def family_list(request):
    families = models.Family.objects.all()
    email = 'jdoepp@gmail.com'
    return render(request, 'families/family_list.html', {'families': families,
        'email':email})

def family_detail(request, pk):
    family = get_object_or_404(models.Family, pk=pk)
    members = chain(family.adult_set.all(), family.dependent_set.all())
    return render(request, 'families/family_detail.html', {'family':family,
        'members': members
        })

def member_detail(request, family_pk, member_pk, member_type):
    if member_type == 'a':
        member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
    else:
        member = get_object_or_404(models.Dependent, family_id=family_pk, pk=member_pk)
    return render(request, 'families/member_detail.html', {'member':member, 'member_type':member_type})

@login_required
def member_create(request, family_pk, member_type):
    family = get_object_or_404(models.Family, pk=family_pk)
    if member_type == 'a':
        form_class = forms.AdultMemberForm
    else:
        form_class = forms.DependentMemberForm

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
        formset = forms.DependentMemberFormSet(queryset=family.dependent_set.all())

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
            formset = forms.DependentMemberFormSet(request.POST, queryset=family.dependent_set.all())
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
    if request.method == 'POST':
        form = forms.FamilyForm(instance=family, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['family_name']))
        return HttpResponseRedirect(reverse('families:detail', kwargs={'pk':pk}))
    return render(request, 'families/family_form.html', {'form': form,
        'family':pk})

@login_required
def member_edit(request, family_pk, member_pk, member_type):
    if member_type == 'a':
        member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
        form_class = forms.AdultMemberForm
    else:
        member = get_object_or_404(models.Dependent, family_id=family_pk, pk=member_pk)
        form_class = forms.DependentMemberForm
    form = form_class(instance=member)

    if request.method == 'POST':
        form = form_class(instance=member, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['first_name']))
        return HttpResponseRedirect(member.get_absolute_url())
    return render(request, 'families/member_form.html', {'form': form, 'family':member.family})

