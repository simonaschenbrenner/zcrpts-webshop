from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import MySignUpForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import MyUser
from django.shortcuts import redirect, render


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


def user_detail(request, **kwargs):
    myuser_id = kwargs['pk']
    current_user = MyUser.objects.get(id=myuser_id)
    print(str(myuser_id))
    context = {'current_user': current_user}
    return render(request, 'user-detail.html', context)


def update_user(request, **kwargs):
    myuser_id = kwargs['pk']
    current_user = MyUser.objects.get(id=myuser_id)
    if request.method == 'POST':
        userForm = EditProfileForm(request.POST, instance=current_user)
        userForm.instance.user = current_user
        if userForm.is_valid():
            userForm.save()
            # print("I saved new game")
        else:
            pass
            print(userForm.errors)

        return redirect('home')

    else:  # request.method == 'GET'
        print("I am in GET")
        userForm = EditProfileForm(instance=current_user)
        context = {'form': userForm}
        return render(request, 'change-user-detail.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # print("I saved new game")
        else:
            pass
            print(form.errors)

        return redirect('home')

    else:  # request.method == 'GET'
        print("I am in GET")
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'change-password.html', context)


