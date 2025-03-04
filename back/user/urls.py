# from django.urls import path
# from . import views

# urlpatterns = [
#     path('registro/', views.register),
#     path('login/', views.login)
# ]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('registro/', views.register),
    path('login/', views.login_view),  # Cambiamos el nombre a login_view
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]