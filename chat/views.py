# chat/views.py
from django.shortcuts import render

from chat.models import chat_room


def room(request):
    article = None
    patient = article.a_patient if article else None

    counselor = request.user.counselor

    room, _ = chat_room.objects.get_or_create(r_article=article, r_counselor=counselor, r_patient=patient)
    room.chat_message_set.all()
    room = chat_room()
    context = {'room': room}
    return render(request, "chat/room.html", context)
