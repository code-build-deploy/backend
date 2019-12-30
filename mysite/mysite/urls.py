"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from app import views as app_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_view.home, name='home'),
    path('login/', app_view.login, name='login'),
    path('display/', app_view.display, name='display'),
    # path('register/new/', app_view.register_user_request, name='registerationrequest'),
    path('register/', app_view.register_user, name='register'),
    path('dashboard/', app_view.dashboard, name='dashboard'),
    path('login/org/', app_view.organisation_login, name='organisation_login'),
    path('register/org/', app_view.register_organisation, name='reg_org'),
    path('certificate/', app_view.create_cert, name='create_certificate'),
    path('certificate/sign/', app_view.sign_certificate, name='sign_certificate'),
    # path('autosave/', app_view.autosave, name='autosave'),
    # path('response/', app_view.create_hash, name='generatehash'),
    # path('clash/', app_view.clash, name='clash'),
]