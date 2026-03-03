from django.urls import path
from .views import dashboard, categories, add_category, edit_category, delete_category, posts, add_post, edit_post, delete_post, users, add_user, edit_user, delete_user


urlpatterns = [
    path('', dashboard, name='dashboard'),
    # category crud
    path('categories/', categories, name='categories'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:pk>/', edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', delete_category, name='delete_category'),
    # post crud
    path('posts/', posts, name='posts'),
    path('posts/add/', add_post, name='add_post'),
    path('posts/edit/<int:pk>', edit_post, name='edit_post'),
    path('posts/delete/<int:pk>', delete_post, name='delete_post'),
    # user
    path('users/', users, name='users'),
    path('users/add/', add_user, name='add_user'),
    path('users/edit/<int:pk>', edit_user, name='edit_user'),
    path('users/delete/<int:pk>', delete_user, name='delete_user'),

]
