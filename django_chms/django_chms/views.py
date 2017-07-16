from django.conf import settings
from django.shortcuts import render

from . import forms

def front_page(request):
    return render(request, 'home.html', {'church_name':settings.CHURCH_NAME, 'image':settings.CHURCH_IMAGE})

