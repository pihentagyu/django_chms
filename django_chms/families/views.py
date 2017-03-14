from django.http import HttpResponse
from django.shortcuts import render

from .models import Family

# Create your views here.

def family_list(request):
    families = Family.objects.all()
    return render(request, 'families/family_list.html', {'families': families})
       

