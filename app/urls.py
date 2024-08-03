from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:theme_name>/', views.theme_view, name='theme'),
    path('autor/<str:name_autor>/', views.profile, name='profile'),
]