from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

_PATIENT_GROUP = 'patient'
_COUNSELOR_GROUP = 'counselor'


class _PermissionTypes:
    _add, _change, _delete, _view = 1, 2, 4, 8

    @property
    def ADD(self):
        return self._add

    @property
    def CHANGE(self):
        return self._change

    @property
    def DELETE(self):
        return self._delete

    @property
    def VIEW(self):
        return self._view

    @property
    def ALL(self):
        return self._add | self._change | self._delete | self._view

    @property
    def iterator(self):
        return self._add, self._change, self._delete, self._view


PermissionType = _PermissionTypes()

_t_str = {PermissionType.ADD: 'add', PermissionType.VIEW: 'view', PermissionType.DELETE: 'delete',
          PermissionType.CHANGE: 'change'}


class _UserGroups:
    @property
    def patient_group(self):
        return Group.objects.get_or_create(name=_PATIENT_GROUP)[0]

    @property
    def counselor_group(self):
        return Group.objects.get_or_create(name=_COUNSELOR_GROUP)[0]


UserGroups = _UserGroups()


def _add_iff_not_exists(group, permissions):
    for permission in permissions:
        if not group.permissions.filter(pk=permission.pk).exists():
            group.permissions.add(permission)
    group.save()


def _get_permissions(content_type, permission_types):
    content_name = content_type.name
    return [
        Permission.objects.get_or_create(
            codename=f'{_t_str[t]}_{content_name}',
            name=f'Can {_t_str[t]} {content_name}',
            content_type=content_type)[0]
        for t in PermissionType.iterator if t & permission_types
    ]


def get_permission_name(model, permission_type):
    contenttype = ContentType.objects.get_for_model(model)
    required_permission = _get_permissions(contenttype, permission_type)[0]
    return f"{contenttype.app_label}.{required_permission.codename}"


def set_permission(**kwargs):
    article_type = ContentType.objects.get(app_label='board', model='article')
    comment_type = ContentType.objects.get(app_label='board', model='comment')
    communication_type = ContentType.objects.get(app_label='board', model='communication')
    counselorreview_type = ContentType.objects.get(app_label='board', model='counselorreview')
    # 환자 회원 권한
    patient_permissions = []
    patient_permissions.extend(_get_permissions(article_type, PermissionType.ALL))
    patient_permissions.extend(_get_permissions(comment_type, PermissionType.ALL))
    patient_permissions.extend(_get_permissions(communication_type, PermissionType.ALL))
    patient_permissions.extend(_get_permissions(counselorreview_type, PermissionType.ALL))
    # 상담사 회원 권한
    counselor_permissions = []
    counselor_permissions.extend(_get_permissions(article_type, PermissionType.VIEW))
    counselor_permissions.extend(_get_permissions(comment_type, PermissionType.ALL))
    counselor_permissions.extend(_get_permissions(counselorreview_type, PermissionType.VIEW))

    _add_iff_not_exists(UserGroups.patient_group, patient_permissions)
    _add_iff_not_exists(UserGroups.counselor_group, counselor_permissions)
