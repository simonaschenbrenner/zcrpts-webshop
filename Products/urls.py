from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.ProductListView.as_view(), name='product-list'),
    #path('show/', views.product_list, name='product-list'),
    #path('show/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/rate/<int:stars>/', views.rate, name='product-rate'),
    path('add/', views.ProductCreateView.as_view(), name='product-create'),
]
