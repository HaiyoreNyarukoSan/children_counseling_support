from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User, Patient, Counselor


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


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    pass


from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django.utils.translation import gettext_lazy as _


class GroupAdmin(DefaultGroupAdmin):
    list_display = ('name', 'get_members')
    readonly_fields = ('get_members',)

    def get_members(self, obj):
        members = obj.user_set.all()
        member_names = [member.username for member in members]
        return ', '.join(member_names)

    get_members.short_description = _('멤버')


# 기존 'GroupAdmin' 클래스를 사용하지 않도록 해제
admin.site.unregister(Group)
# 커스텀한 `GroupAdmin` 클래스로 등록
admin.site.register(Group, GroupAdmin)
