from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(rol):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('rescateComida:login')
            
            if request.user.tipo_usuario != rol:
                messages.error(request, 'No tienes permiso para acceder aquí')
                return redirect('rescateComida:home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
