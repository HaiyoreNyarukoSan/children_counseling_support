from django.shortcuts import render, redirect

from board.forms import CounselorReviewForm
from .forms import RoomForm
from .models import chat_room, chat_message
from board.models import Article
from users.models import Counselor, Patient


def room_patient(request):
    if request.method == 'POST':
        room_form = RoomForm(data=request.POST, files=request.FILES)
        counselor_id = request.POST.get('counselor_id')
        counselor = Counselor.objects.get(pk=counselor_id)

        if room_form.is_valid():
            # room = room_form.save(commit=False)
            patient = room_form.cleaned_data["r_patient"]
            room, _ = chat_room.objects.get_or_create(r_patient=patient, r_counselor=counselor)
            chatmessages = room.chat_message_set.all()
            chatmessage = ""
            for cmessage in chatmessages:
                nickname = cmessage.m_writer.u_nickname
                message = cmessage.m_content
                chatmessage += f"{nickname}: {message}\n"
    
            context = {'room': room, 'chatmessage': chatmessage}
            return render(request, "chat/room.html", context)


def room_counselor(request):
    # input type = article.a_patient_id
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        counselor = request.user.counselor  # 로그인 상태
        room, _ = chat_room.objects.get_or_create(r_patient=patient, r_counselor=counselor)
        chatmessages = room.chat_message_set.all()
        chatmessage = ""
        for cmessage in chatmessages:
            nickname = cmessage.m_writer.u_nickname
            message = cmessage.m_content
            chatmessage += f"{nickname}: {message}\n"

        context = {'room': room, 'chatmessage': chatmessage}
        return render(request, "chat/room.html", context)
