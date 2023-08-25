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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from board import views
from children_counseling_support import settings

urlpatterns = [
    path("", views.main, name='home'),
    path("Counselor-list/", views.cs_list, name='Counselor-list'),
    path("Counselor-detail/<int:id>", views.cs_detail, name='Counselor-detail'),
    path("User_security/", TemplateView.as_view(template_name='User_security.html'), name='User_security'),
    path("ChatBot/", TemplateView.as_view(template_name='ChatBot.html'), name='ChatBot'),
    path("My-Page/", TemplateView.as_view(template_name='My-Page.html'), name='My-Page'),
    path("Picture-list", views.a_list, name='Picture-list'),
    path("Picture-create", views.a_create, name='Picture-create'),
    path("Communication-Create/", views.c_create, name='Communication-Create'),
    path("Communication-List/", views.c_list, name='Communication-List'),
    path("Communication-detail/<int:id>", views.c_detail, name='Communication-detail'),
    path("Picture-detail/<int:id>", views.a_detail, name='Picture-detail'),
    path("admin/", admin.site.urls),
    path("board/", include('board.urls')),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        prefix=settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
