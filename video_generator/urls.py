"""
URL configuration for video_generator project.

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
from . import views
from rest_framework import routers

from .allauth_views import (
    AllauthRegisterView, AllauthLoginView, AllauthLogoutView,
    AllauthUserView, AllauthUpdateUserView, AllauthChangePasswordView
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r'words', views.WordViewSet, basename='word')
router.register(r'texts', views.TextViewSet, basename='text')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', AllauthRegisterView.as_view(), name='register'),
    path('api/auth/login/', AllauthLoginView.as_view(), name='login'),
    path('api/auth/logout/', AllauthLogoutView.as_view(), name='logout'),
    path('api/auth/user/', AllauthUserView.as_view(), name='user'),
    path('api/auth/user/update/', AllauthUpdateUserView.as_view(), name='update_user'),
    path('api/auth/password/change/', AllauthChangePasswordView.as_view(), name='change_password'),

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('api/', include('video_generator.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path('', views.home, name='home'),  # Root URL
]
