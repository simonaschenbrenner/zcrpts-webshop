from django.urls import path
from Carts import views

urlpatterns = [
    path('show/', views.ProductListView.as_view(), name='cart-list'),
    #path('show/', views.product_list, name='product-list'),
    #path('show/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='product-vote'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),
]
