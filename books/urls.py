"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.http import request
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib import messages
from users.views import Login

import library

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('base/', TemplateView.as_view(template_name='base-menu.html'), name='base'),
    path('', include('library.urls', namespace='library')),
    path('register/', user_views.register, name='register'),
    path('login/', Login.as_view(), name='login'),
    path('account/', user_views.user_account, name='user-account'),
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('account/password-change/', user_views.PasswordChange.as_view(), name='password-change'),

]
