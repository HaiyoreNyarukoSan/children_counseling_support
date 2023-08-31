from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.forms import modelformset_factory

from users.models import User, Patient, Counselor


def widget_attr(widget_class='form-control', placeholder='', title='', required=True):
    return {
        'class': widget_class,
        'placeholder': placeholder,
        # 'autocomplete': 'off',
        'required': required,
        'title': title,
    }


id_widget_attr = widget_attr(placeholder='ID', title='아이디를 입력하세요')
password_widget_attr = widget_attr(placeholder='Password', title='비밀번호를 입력하세요')
password_confirm_widget_attr = widget_attr(placeholder='Password Confirm', title='비밀번호를 다시 입력하세요')
old_password_widget_attr = widget_attr(placeholder='Current Password', title='현재 사용 중인 비밀번호를 입력하세요')
new_password_widget_attr = widget_attr(placeholder='New Password', title='새로 사용할 비밀번호를 입력하세요')
new_password_confirm_widget_attr = widget_attr(placeholder='New Password Confirm', title='새로 사용할 비밀번호를 다시 입력하세요')

nickname_widget_attr = widget_attr(placeholder='u_nickname', title='별명을 입력하세요')
last_name_widget_attr = widget_attr(placeholder='Family Name', title='성씨를 입력하세요')
first_name_widget_attr = widget_attr(placeholder='Given Name', title='이름을 입력하세요')
patient_name_widget_attr = widget_attr(placeholder='Name', title='자식분의 이름을 입력하세요')

email_widget_attr = widget_attr(placeholder='e-mail', title='e-mail을 입력하세요')
birthday_widget_attr = widget_attr(widget_class='btn', title='생일을 입력하세요')
gender_widget_attr = widget_attr(widget_class='', title='성별을 입력하세요')
contact_widget_attr = widget_attr(placeholder='숫자만 입력해주세요', title='전화번호를 입력하세요')

department_widget_attr = widget_attr(placeholder='전문 분야', title='전문 분야를 입력하세요')
resume_widget_attr = widget_attr(placeholder='이력', title='이력을 입력하세요')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'
        self.fields['username'].widget.attrs.update(id_widget_attr)
        self.fields['password'].widget.attrs.update(password_widget_attr)

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(id_widget_attr)
        self.fields['u_nickname'].widget.attrs.update(nickname_widget_attr)
        self.fields['last_name'].widget.attrs.update(last_name_widget_attr)
        self.fields['first_name'].widget.attrs.update(first_name_widget_attr)
        self.fields['password1'].widget.attrs.update(password_widget_attr)
        self.fields['password2'].widget.attrs.update(password_confirm_widget_attr)
        self.fields['email'].widget.attrs.update(email_widget_attr)
        self.fields['u_birthday'].widget.attrs.update(birthday_widget_attr)

    # email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = (
            'username', 'u_nickname', 'last_name', 'first_name', 'u_gender', 'password1', 'password2', 'u_birthday',
            'u_contact', 'email')

        labels = {
            'username': '아이디',
            'u_nickname': '별명',
            'last_name': '성',
            'first_name': '이름',
            'password2': '비밀번호',
            'password2': '비밀번호 확인',
            'u_birthday': '생년월일',
            'u_gender': '성별',
            'u_contact': '전화번호',
        }

        widgets = {
            'u_birthday': forms.SelectDateWidget(
                years=range(1900, date.today().year + 1),
                attrs=birthday_widget_attr,
            ),
            'u_gender': forms.RadioSelect(
                attrs=gender_widget_attr,
            ),
            'u_contact': forms.TextInput(
                attrs=contact_widget_attr,
            ),
        }


class PatientSignUpForm(forms.ModelForm):
    class Meta:
        child_age = 19
        model = Patient
        fields = ('p_name', 'p_gender', 'p_birthday')

        labels = {
            'p_name': '이름',
            'p_gender': '성별',
            'p_birthday': '생년월일',
        }

        widgets = {
            'p_name': forms.TextInput(
                attrs=patient_name_widget_attr,
            ),
            'p_gender': forms.RadioSelect(
                attrs=gender_widget_attr,
            ),
            'p_birthday': forms.SelectDateWidget(
                years=range(date.today().year - child_age, date.today().year + 1),
                attrs=birthday_widget_attr,
            ),
        }


patient_form_set = modelformset_factory(
    Patient,
    form=PatientSignUpForm,
    extra=0,  # Set 'extra' to 0 to allow dynamic form count
)
patient_new_form_set = modelformset_factory(
    Patient,
    form=PatientSignUpForm,
    extra=1,  # Set 'extra' to 0 to allow dynamic form count
)


class CounselorSignUpForm(forms.ModelForm):
    class Meta:
        child_age = 19
        model = Counselor
        fields = ('c_certificate', 'c_department', 'c_resume')

        labels = {
            'c_certificate': '자격증',
            'c_department': '전문 분야',
            'c_resume': '이력',
        }

        widgets = {
            'c_department': forms.TextInput(
                attrs=department_widget_attr,
            ),
            'c_resume': forms.Textarea(
                attrs=resume_widget_attr,
            ),
        }


class ChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['u_nickname'].label = '별명'
        self.fields['u_nickname'].widget.attrs.update(nickname_widget_attr)
        self.fields['email'].widget.attrs.update(email_widget_attr)

    class Meta:
        model = User
        fields = ('u_nickname', 'u_contact', 'email')

        labels = {
            'u_contact': '전화번호',
        }

        widgets = {
            'u_contact': forms.TextInput(
                attrs=contact_widget_attr
            ),
        }


class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = '비밀번호'
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['old_password'].widget.attrs.update(nickname_widget_attr)
        self.fields['new_password1'].widget.attrs.update(new_password_widget_attr)
        self.fields['new_password2'].widget.attrs.update(new_password_confirm_widget_attr)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
