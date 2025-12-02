from django.shortcuts import redirect
from django.urls import reverse

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = [
            reverse('rescateComida:home'),
            reverse('rescateComida:login'),
            reverse('rescateComida:registro'),
        ]
        
        protected_patterns = [
            '/cliente/',
            '/proveedor/',
            '/adminpanel/',
        ]
        
        requires_auth = any(request.path.startswith(pattern) for pattern in protected_patterns)
        
        if requires_auth and not request.user.is_authenticated:
            return redirect('rescateComida:login')
        
        response = self.get_response(request)
        return response
