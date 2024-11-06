# bono/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import BonoViewSet, GeneratedBonoViewSet, UserViewSet
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bonos', BonoViewSet, basename='bono')
router.register(r'users', UserViewSet, basename='user')
router.register(r'generated-bonos', GeneratedBonoViewSet, basename='generated-bono')

urlpatterns = [
    path('', include(router.urls)),

    # path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', views.user_login, name='login'),
]
