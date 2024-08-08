from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('temas/<str:theme_name>/', views.theme_view, name='theme'),
    path('autor/<str:name_autor>/', views.profile, name='profile'),
    path('registro/', views.register, name='registro'),
    path("logout/", views.unlogin, name="cerrar"),
    path("login/", views.login, name="login"),
    path("create_post/", views.create_post, name="create_post"),
    path("<int:pk>/", views.view_post, name="view_post"),
]