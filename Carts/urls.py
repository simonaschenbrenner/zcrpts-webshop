from django.urls import path
from . import views

urlpatterns = [
        path('', views.show_shopping_cart, name='show-shopping-cart'),
        path('pay/', views.pay, name='shopping-cart-pay'),
]
