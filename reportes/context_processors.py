from django.conf import settings


def enable_reports(request):
    return {"enable_reports": getattr(settings, "ENABLE_REPORTS", False)}
