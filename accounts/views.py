from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm#, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.views.generic import FormView, RedirectView, DetailView, CreateView

from families.models import Family
from . import forms

class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("families:family_list")
    template_name = 'accounts/login.html'

    def get_form(self, form_class=None):
        if form_class == None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(CreateView):
    #form_class = UserCreationForm
    form_class = forms.UserSignUpForm 
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        save_form = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        return save_form


@login_required
def profile_view(request):
    try:
        family = Family.objects.select_related('user').get(user=request.user.id)
    except ObjectDoesNotExist:
        family = None
    if family:
        return render_to_response('accounts/profile.html', {'user': request.user, 'family_pk':family.pk})
    else:
        return render_to_response('accounts/profile.html', {'user': request.user, 'family_pk':None})
