from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MySignUpView.as_view(), name='signup'),
    path('myuser-list/', views.MyUserListView.as_view(), name='myuser-list'),
    path('show/<int:pk>/', views.user_detail, name='myuser-detail'),
    path('show/<int:pk>/edit/', views.update_user, name='change-user-detail'),
    path('change-password/', views.change_password, name='change-password'),
]
