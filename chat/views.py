from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .forms import RoomForm
from .models import chat_room
from users.models import Counselor, Patient


def room_patient(request):
    if request.method == 'POST':
        room_form = RoomForm(data=request.POST, files=request.FILES)
        counselor_id = request.POST.get('counselor_id')
        counselor = Counselor.objects.get(pk=counselor_id)

        if room_form.is_valid():
            patient = room_form.cleaned_data["r_patient"]
            room, _ = chat_room.objects.get_or_create(r_patient=patient, r_counselor=counselor)
            return enter_room(request, room)
    raise PermissionDenied


def room_counselor(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        counselor = request.user.counselor  # 로그인 상태
        room, _ = chat_room.objects.get_or_create(r_patient=patient, r_counselor=counselor)
        return enter_room(request, room)
    raise PermissionDenied


def get_room(request, room_id):
    room = get_object_or_404(chat_room, pk=room_id)
    return enter_room(request, room)


def enter_room(request, room):
    counselor_user_id = room.r_counselor.c_user_id
    patient_user_id = room.r_patient.p_user_id
    if not request.user.id in (counselor_user_id, patient_user_id): raise PermissionDenied
    chatmessages = room.chat_message_set.all()
    chatmessage = ""
    for cmessage in chatmessages:
        nickname = cmessage.m_writer.u_nickname
        message = cmessage.m_content
        chatmessage += f"{nickname}: {message}\n"

    context = {'room': room, 'chatmessage': chatmessage}
    return render(request, "chat/room.html", context)


@login_required(login_url='users:choose_your_type', redirect_field_name='board:chat_room_list')
def chat_room_list(request):
    rooms = chat_room.objects.filter(Q(r_patient__p_user_id=request.user.id) | Q(
        r_counselor__c_user_id=request.user.id)).order_by('-id')

    room_per_page = 2

    paginator = Paginator(rooms, room_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page}
    return render(request, 'chat/chat_list.html', context)
