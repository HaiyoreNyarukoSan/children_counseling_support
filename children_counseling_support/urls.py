"""children_counseling_support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='Main.html'), name='home'),
    path("Patient-Login/", TemplateView.as_view(template_name='Patient-Login.html'), name='Patient-Login'),
    path("Counselor-Login/", TemplateView.as_view(template_name='Counselor-Login.html'), name='Counselor-Login'),
    path("Patient-signup/", TemplateView.as_view(template_name='Patient-signup.html'), name='Patient-signup'),
    path("Counselor-signup/", TemplateView.as_view(template_name='Counselor-signup.html'), name='Counselor-signup'),
    path("Counselor-list/", TemplateView.as_view(template_name='Counselor-list.html'), name='Counselor-list'),
    path("Counselor-detail/", TemplateView.as_view(template_name='Counselor-detail.html'), name='Counselor-detail'),
    path("User_security/", TemplateView.as_view(template_name='User_security.html'), name='User_security'),
    path("ChatBot/", TemplateView.as_view(template_name='ChatBot.html'), name='ChatBot'),
    path("Picture-list", TemplateView.as_view(template_name='Picture-list.html'), name='Picture-list'),
    path("admin/", admin.site.urls),
]
