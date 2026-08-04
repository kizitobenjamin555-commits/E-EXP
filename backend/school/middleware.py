from django.http import JsonResponse

class ForcePasswordChangeMiddleware:
    """Middleware that prevents users who must change their password from accessing most of the site
    until they change it. Allows access to the password change endpoint, admin login pages, and static/media.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = [
            '/api/password/change/',
            '/admin/login/',
            '/admin/logout/',
            '/static/',
            '/media/',
            '/api/upload/csv/dry-run/',
            '/api/upload/csv/',
        ]

    def __call__(self, request):
        user = getattr(request, 'user', None)
        path = request.path
        # Allow if not authenticated or staff (admin)
        if user and user.is_authenticated and not user.is_staff and getattr(user, 'must_change_password', False):
            # allow if path starts with any allowed path
            if not any(path.startswith(p) for p in self.allowed_paths):
                return JsonResponse({'detail': 'Password change required', 'change_url': '/api/password/change/'}, status=403)
        response = self.get_response(request)
        return response
