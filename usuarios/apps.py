from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"

    def ready(self):
        from django.contrib.auth.models import Group, Permission

        administrador, _ = Group.objects.get_or_create(name="Administrador")
        usuario, _ = Group.objects.get_or_create(name="Usuario")

        admin_permissions = Permission.objects.filter(
            content_type__app_label="auth",
            content_type__model="user",
        )
        administrador.permissions.set(admin_permissions)
