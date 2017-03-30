from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

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

def adult_detail(request, family_pk, member_pk):
    member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
    return render(request, 'families/member_detail.html', {'member':member})

def dependent_detail(request, family_pk, member_pk):
    member = get_object_or_404(models.Dependent, family_id=family_pk, pk=member_pk)
    return render(request, 'families/member_detail.html', {'member':member})

@login_required
def adult_member_create(request, family_pk):
    family = get_object_or_404(models.Family, pk=family_pk)
    form = forms.AdultMemberForm()

    if request.method == 'POST':
        form = forms.AdultMemberForm(request.POST)
        if form.is_valid():
            adult = form.save(commit=False)
            adult.family = family
            adult.save()
            messages.add_message(request, messages.SUCCESS, 
                    "Adult Family Member added!")
            return HttpResponseRedirect(adult.get_absolute_url())
    return render(request, 'families/adult_member_form.html', {'form': form,
        'family':family})

@login_required
def adult_member_edit(request, family_pk, member_pk):
    adult_member = get_object_or_404(models.Adult, family_id=family_pk, pk=member_pk)
    form = forms.AdultMemberForm(instance=adult_member)
    return render(request, 'families/adult_member_form.html', {'form': form,
        'family':adult_member.family})

