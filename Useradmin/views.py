from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import MySignUpForm
from .models import MyUser


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in. PERFORM CUSTOM CODE."""
        auth_login(self.request, form.get_user())
        # form.get_user().execute_after_login()  # Custom code
        return HttpResponseRedirect(self.get_success_url())


# TODO in Profilansicht ändern
class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_users'
    template_name = 'myuser-list.html'

# TODO Kundenservicebereich als Erweiterung der Profilansicht
class ManagerView(generic.TemplateView):
    def get_context_data(self, **kwargs):
        myuser = self.request.user
        is_manager = False
        if myuser.is_authenticated:  # Anonymous user cannot be manager
            is_manager = myuser.is_manager or myuser.is_superuser  # TODO superuser automatisch auch manager

        context = super(ManagerView, self).get_context_data(**kwargs)
        context['is_manager'] = is_manager
        return context
