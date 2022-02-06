from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .forms import MySignUpForm, EditProfileForm
from .models import MyUser


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
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

        user_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        user_form.instance.user = current_user
        if user_form.is_valid():
            user_form.save()

        else:
            print(user_form.errors)
        return redirect('home')

    else:  # request.method == 'GET'
        user_form = EditProfileForm(instance=current_user)
        context = {'form': user_form}
        return render(request, 'change-user-detail.html', context)


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
        else:
            print(form.errors)
        return redirect('home')

    else:  # request.method == 'GET'
        print("I am in GET")
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'change-password.html', context)

