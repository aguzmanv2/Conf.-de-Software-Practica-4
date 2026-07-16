import csv
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth.models import User
from usuarios.decorators import admin_required


@admin_required
def exportar_usuarios_csv(request):
    if not getattr(settings, "ENABLE_REPORTS", False):
        raise Http404

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="usuarios.csv"'

    writer = csv.writer(response)
    writer.writerow(["Nombres", "Apellidos", "Email"])

    for usuario in User.objects.all().order_by("-date_joined"):
        writer.writerow([usuario.first_name, usuario.last_name, usuario.email])

    return response
