from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.groups.filter(name="Administrador").exists():
            messages.error(request, "No tienes permiso para acceder a esta sección.")
            return redirect("bienvenida")
        return view_func(request, *args, **kwargs)
    return wrapper
