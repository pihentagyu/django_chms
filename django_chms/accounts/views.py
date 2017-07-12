from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, RedirectView


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("families:list")
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

