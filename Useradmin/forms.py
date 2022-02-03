from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser



class MySignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
    # password ist in UserCreationForm schon mit dabei


class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = MyUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
        )

