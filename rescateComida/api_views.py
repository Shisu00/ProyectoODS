from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.filter(estado='disponible')
    serializer_class = ProductoSerializer



@require_GET
def api_externa(request):
    url = 'https://jsonplaceholder.typicode.com/posts' 
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        return JsonResponse(r.json(), safe=False)
    else:
        return JsonResponse({'error': 'No se pudo obtener datos'}, status=500)