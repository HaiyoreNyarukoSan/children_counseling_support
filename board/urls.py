from django.contrib import admin
from django.urls import path, include

from board import views

app_name = 'board'

urlpatterns = [
    path("", lambda i: i),
    path("Picture-detail/<int:id>", views.a_detail, name='a_detail'),
    path("Picture-list", views.a_list, name='a_list'),
    path("Picture-create", views.a_create, name='a_create'),
    path("Communication-List", views.c_list, name='c_list'),
    path("Communication-Create", views.c_create, name='c_create'),
    path("Communication-detail/<int:id>", views.c_detail, name='c_detail'),
    path("Counselor-list/", views.cs_list, name='cs-list'),
    path("Counselor-detail/<int:id>", views.cs_detail, name='cs_detail'),
    # 172.0.0.1/board/Picture-create
    # board:a_create
    # -> view.a_create(request)
]
