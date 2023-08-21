from django.contrib import admin

from board.models import Article
from users.models import User, Patient


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        ("개인정보", {"fields": ("first_name", "last_name", "email")}),
        # ("추가필드", {"fields": ("u_birthday", "u_gender", "u_gender")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("중요한 일정", {"fields": ("last_login", "date_joined")}),
    ]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass
