from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from .forms import RegistroForm, EditarPerfilForm, EditarUsuarioForm
from .decorators import admin_required
from .jwt_utils import generate_jwt


def login_view(request):
    if request.user.is_authenticated:
        return redirect("bienvenida")

    error = None
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if getattr(settings, "ENABLE_JWT", False):
                token = generate_jwt(user.id)
                response = redirect("bienvenida")
                response.set_cookie(
                    getattr(settings, "JWT_COOKIE_NAME", "jwt_token"),
                    token,
                    max_age=getattr(settings, "JWT_EXPIRATION_HOURS", 2) * 3600,
                    httponly=True,
                )
                return response
            return redirect("bienvenida")
        else:
            error = "Email o contraseña incorrectos."

    return render(request, "usuarios/login.html", {"error": error})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect("bienvenida")

    form = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora inicia sesión.")
            return redirect("login")

    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def bienvenida_view(request):
    return render(request, "usuarios/bienvenida.html")


@login_required
def editar_perfil_view(request):
    form = EditarPerfilForm(instance=request.user)
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("editar_perfil")

    return render(request, "usuarios/editar_perfil.html", {"form": form})


@admin_required
def usuarios_lista_view(request):
    usuarios = User.objects.all().order_by("-date_joined")
    grupos = Group.objects.all()

    for usuario in usuarios:
        grupo = usuario.groups.first()
        if request.method == "POST" and f"rol_{usuario.id}" in request.POST:
            rol_id = request.POST.get(f"rol_{usuario.id}")
            if rol_id:
                grupo = Group.objects.get(id=int(rol_id))
                usuario.groups.clear()
                usuario.groups.add(grupo)
                messages.success(
                    request,
                    f"Rol de {usuario.get_full_name() or usuario.email} actualizado a {grupo.name}.",
                )
                return redirect("usuarios_lista")

    return render(
        request,
        "usuarios/usuarios_lista.html",
        {"usuarios": usuarios, "grupos": grupos},
    )


@admin_required
def editar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    form = EditarUsuarioForm(instance=usuario)
    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("usuarios_lista")

    return render(
        request,
        "usuarios/editar_usuario.html",
        {"form": form, "usuario": usuario},
    )


@admin_required
def eliminar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("usuarios_lista")

    return render(
        request,
        "usuarios/eliminar_usuario.html",
        {"usuario": usuario},
    )


def logout_view(request):
    logout(request)
    response = redirect("login")
    if getattr(settings, "ENABLE_JWT", False):
        response.delete_cookie(getattr(settings, "JWT_COOKIE_NAME", "jwt_token"))
    return response
