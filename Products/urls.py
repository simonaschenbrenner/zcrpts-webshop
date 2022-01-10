from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.product_create, name='product-create'),
    path('show/', views.product_list, name='product-list'),
    # TODO need search url?
    path('show/<str:search_term>/<int:min_stars>/', views.product_search, name='product-search'),
    path('show/<int:pk>/', views.product_detail, name='product-detail'),
    path('show/<int:pk>/rate/<int:stars>/', views.rate, name='product-rate'),
    path('show/<int:pk>/comment/<int:commentid>/vote/<str:is_helpful>/', views.vote, name='comment-vote'),
    path('download/<int:pk>/', views.download_license, name='download-license'),
    path('comments', views.comment_list, name='comment-list'),
    path('flag/<int:pk>/comment/<int:commentid>', views.flag, name='comment-flag'),
    path('delete/<int:pk>/comment/<int:commentid>', views.comment_delete, name='comment-delete'),
    # path('update/<int:pk>/comment/<int:commentid>', views.comment_update, name='comment-update'),
    path('show/<int:pk>/edit/<int:commentid>', views.update_review, name='review-update'),
    # path('show/<int:pk>/flag/<bool:flag>', views.flag, name='comment-flag'),
]
