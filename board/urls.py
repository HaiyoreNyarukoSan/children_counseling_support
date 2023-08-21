from django.contrib import admin
from django.urls import path, include

app_name = 'borard'

urlpatterns = [
    path("", lambda i: i),
]
