"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@csrf_exempt
def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({"status": "ok", "service": "adaptaki"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', health_check, name='health_check'),

    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User endpoints
    path('api/users/', include('users.urls')),

    # Graph endpoints
    path('api/graph/', include('graph.urls')),

    # Questions endpoints
    path('api/questions/', include('questions.urls')),

    # Exams endpoints
    path('api/exams/', include('exams.urls')),

    # Lectures endpoints
    path('api/lectures/', include('lectures.urls')),

    # Social Auth endpoints
    path('social-auth/', include('social_django.urls', namespace='social')),
]
