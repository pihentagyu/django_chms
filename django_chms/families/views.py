from django.shortcuts import get_object_or_404, render

from .models import Family, Member

# Create your views here.

def family_list(request):
    families = Family.objects.all()
    return render(request, 'families/family_list.html', {'families': families})

def family_detail(request, pk):
    family = get_object_or_404(Family, pk=pk)
    return render(request, 'families/family_detail.html', {'family':family})

def member_detail(request, family_pk, member_pk):
    member = get_object_or_404(Member, family_id=family_pk, pk=member_pk)
    return render(request, 'families/member_detail.html', {'member':member})
