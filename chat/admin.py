from django.contrib import admin

from chat.models import chat_room


@admin.register(chat_room)
class chat_roomAdmin(admin.ModelAdmin):
    pass
