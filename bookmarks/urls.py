from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('show/', views.show_bookmarks, name='show'),
    path('add/', views.add_bookmark, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
