from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/exportar/", views.exportar_usuarios_csv, name="exportar_usuarios"),
]
