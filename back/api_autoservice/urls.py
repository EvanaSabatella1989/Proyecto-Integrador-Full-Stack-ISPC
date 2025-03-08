"""
URL configuration for api_autoservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from servicio.models import Servicio
from reserva.models import Reserva

from servicio.serializer import ServicioSerializer
from servicio import views

from categoria.views import CategoriaUpdateDelete, categoriaList

from carrito.views import Carrito


from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'servicio', views.ServicioViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('servicio.urls')),
    path('api/', include('producto.urls')),
    path('api/venta/', include('venta.urls')),
    path('api/', include('reserva.urls')),
     path('api/', include('sucursal.urls')),

    # path('api/', include('servicio.urls')),
    # path('api/servicio/servicioList/',views.servicioList),
    # path('api/servicio/delete/<pk>/', ServicioUpdateDelete.as_view()),
    path('api/', include('categoria.urls')),
    path('api/categoria/<pk>/', categoriaList),
    path('api/categoria/update/<pk>/', categoriaList),
    path('api/categoria/', categoriaList),
    path('api/categoria/detail/<pk>/', categoriaList),

    path('api/', include('carrito.urls'))
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# para que cargue la foto
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
