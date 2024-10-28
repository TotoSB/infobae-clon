from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('temas/<str:theme_name>/', views.theme_view, name='theme'),
    path('sub_temas/<str:theme_name>/', views.subtheme_view, name='sub_theme'),
    path("temas/<str:theme_name>/<int:pk>/", views.view_post, name="view_post"),
    path('autor/<str:name_autor>/', views.profile, name='profile'),
    path('registro/', views.register, name='registro'),
    path("logout/", views.unlogin, name="cerrar"),
    path("login/", views.login, name="login"),
    path("create_post/", views.create_post, name="create_post"),
    path("edit_post/<int:pk>/", views.edit_post, name="edit_post"),
    path("delete_post/<int:pk>/", views.delete_post, name="delete_post"),
    path("search_post/", views.search, name="search_post"),
    path("save_post/<int:post_id>/", views.save_post, name="save_post"),
    path("guardados/", views.bookmarks, name="guardados"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("make_staff/<int:usuario_id>/", views.make_staff, name="make_staff")
]