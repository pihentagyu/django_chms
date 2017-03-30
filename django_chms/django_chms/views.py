from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from . import forms

def front_page(request):
    return render(request, 'home.html')

def suggestion_view(request):
    form = forms.SuggestionForm()
    if request.method == 'POST':
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                    'Suggestion from {}'.format(form.cleaned_data['name']),
                    form.cleaned_data['suggestions'],
                    '{name} <{email}>'.format(**form.cleaned_data),
                    ['jdoepp@gmail.com'])
            messages.add_message(request, messages.SUCCESS, 'Thanks for your suggestion')
            print('good form')
            return HttpResponseRedirect(reverse('suggestion'))
    return render(request, 'suggestion_form.html', {'form':form})
