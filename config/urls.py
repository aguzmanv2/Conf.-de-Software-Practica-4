from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from usuarios import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_view, name="inicio"),
    path("login/", views.login_view, name="login"),
    path("registro/", views.registro_view, name="registro"),
    path("bienvenida/", views.bienvenida_view, name="bienvenida"),
    path("perfil/", views.editar_perfil_view, name="editar_perfil"),
    path("usuarios/", views.usuarios_lista_view, name="usuarios_lista"),
    path("usuarios/<int:usuario_id>/editar/", views.editar_usuario_view, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/eliminar/", views.eliminar_usuario_view, name="eliminar_usuario"),
    path("logout/", views.logout_view, name="logout"),
]

if getattr(settings, "ENABLE_REPORTS", False):
    urlpatterns += [
        path("reportes/", include("reportes.urls")),
    ]
