"""bulletin URL Configuration

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

from . import views
from .views import login_patient_view, login_counselor_view, signup_patient, signup_counselor, logout_view, change, \
    my_page, change_information, change_password

app_name = "users"

urlpatterns = [
    path('login/patient', login_patient_view, name="login-patient"),
    path('login/counselor', login_counselor_view, name="login-counselor"),
    path('signup/choose_your_type', TemplateView.as_view(template_name='users/Choose-Your-Type.html'),
         name="choose_your_type"),
    path('signup/patient', signup_patient, name="signup-patient"),
    path('signup/counselor', signup_counselor, name="signup-counselor"),
    path('logout', logout_view, name="logout"),
    path('change', TemplateView.as_view(template_name='users/choose_your_change.html'), name="change"),
    path('change/information', change_information, name="change_information"),
    path('change/password', change_password, name="change_password"),
    path("My-Page/", my_page, name='My-Page'),
]
