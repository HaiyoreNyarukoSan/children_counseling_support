# chat/urls.py
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path("patient", views.room_patient, name="patient_room"),
    path("counselor", views.room_counselor, name="counselor_room"),
    path("get_room/<int:room_id>", views.get_room, name="get_room"),
    path("my_rooms", views.chat_room_list, name="my_rooms"),
]
