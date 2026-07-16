from django.shortcuts import redirect
from django.conf import settings
from .jwt_utils import decode_jwt


class JwtValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_cookie_name = getattr(settings, "JWT_COOKIE_NAME", "jwt_token")
        token = request.COOKIES.get(jwt_cookie_name)

        if token:
            payload = decode_jwt(token)
            if payload is None:
                response = redirect("login")
                response.delete_cookie(jwt_cookie_name)
                return response

        response = self.get_response(request)
        return response
