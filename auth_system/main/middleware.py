from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Pages that DO NOT require login
        allowed_names = [
            "main:home",
            "main:registration",
            "main:login",  # for login logic
        ]

        # Allow everything under /admin/ (all admin URLs)
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Allow static files
        if request.path.startswith(settings.STATIC_URL):
            return self.get_response(request)

        # Check view name for normal URLs
        try:
            current_url = resolve(request.path_info).view_name
        except:
            current_url = None

        if not request.user.is_authenticated and current_url not in allowed_names:
            return redirect(f"{reverse('main:home')}?next={request.path}")

        return self.get_response(request)


