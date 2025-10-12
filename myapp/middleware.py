# yourapp/middleware.py
from django.utils import timezone

class SessionActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.session['last_seen'] = timezone.now().isoformat()
        return response
