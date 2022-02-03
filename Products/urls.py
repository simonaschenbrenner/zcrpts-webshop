from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.product_create, name='product-create'),
    path('', views.product_list, name='product-list'),
    path('show/<int:pid>/', views.product_detail, name='product-detail'),
    path('edit/<int:pid>', views.product_create, name='product-edit'),
    # TODO download URL
    # path('download/<int:pk>/',
    #      views.download_license, name='download-license'),
    path('comments/all', views.comment_list_all, name='comment-list-all'),
    path('comments/flagged',
         views.comment_list_flagged, name='comment-list-flagged'),
    path('comments/flag/<int:pid>/<int:cid>',
         views.comment_flag, name='comment-flag'),
    path('comments/unflag/<int:cid>',
         views.comment_unflag, name='comment-unflag'),
    path('comments/vote/<int:pid>/<int:cid>/<str:up_or_down>/',
         views.comment_vote, name='comment-vote'),
    path('comments/edit/<int:pid>/<int:cid>',
         views.comment_edit, name='comment-edit'),
    path('comments/delete/<int:pid>/<int:cid>',
         views.comment_delete, name='comment-delete'),
    path('comments/delete/<int:cid>',
         views.comment_delete, name='comment-delete'),
]
