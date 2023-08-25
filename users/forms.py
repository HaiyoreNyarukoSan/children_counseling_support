from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import modelformset_factory

from users.models import User, Patient, Counselor


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ID',
            # 'autocomplete': 'off',
            'required': True,
            'title': '아이디를 입력하세요',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            # 'autocomplete': 'off',
            'required': True,
            'title': '비밀번호를 입력하세요',
        })

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['u_nickname'].label = '별명'
        self.fields['last_name'].label = '성'
        self.fields['first_name'].label = '이름'
        self.fields['password2'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ID',
            # 'autocomplete': 'off',
            'required': True,
            'title': '아이디를 입력하세요',
        })
        self.fields['u_nickname'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nickname',
            # 'autocomplete': 'off',
            'required': True,
            'title': '별명을 입력하세요'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Family Name',
            # 'autocomplete': 'off',
            'required': True,
            'title': '성씨를 입력하세요'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Given Name',
            # 'autocomplete': 'off',
            'required': True,
            'title': '이름을 입력하세요',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            # 'autocomplete': 'off',
            'required': True,
            'title': '비밀번호를 입력하세요',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password Confirm',
            # 'autocomplete': 'off',
            'required': True,
            'title': '비밀번호를 다시 입력하세요',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e-mail',
            # 'autocomplete': 'off',
            'required': True,
            'title': 'e-mail을 입력하세요',
        })

    # email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = (
            'username', 'u_nickname', 'last_name', 'first_name', 'u_gender', 'password1', 'password2', 'u_birthday',
            'u_contact', 'email')

        labels = {
            'u_birthday': '생년월일',
            'u_gender': '성별',
            'u_contact': '전화번호',
        }

        widgets = {
            'u_birthday': forms.SelectDateWidget(
                years=range(1900, date.today().year + 1),
                attrs={
                    # 'class': 'form-control',
                    'required': True,
                    'title': '생일을 입력하세요',
                },
            ),
            'u_gender': forms.RadioSelect(
                attrs={
                    # 'class': 'form-control',
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '성별을 입력하세요',
                },
            ),
            'u_contact': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "000-0000-0000",
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '전화번호를 입력하세요',
                }
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
                attrs={
                    'class': 'form-control',
                    'placeholder': "이름",
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '자식분의 이름을 입력하세요',
                }
            ),
            'p_gender': forms.RadioSelect(
                attrs={
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '성별을 입력하세요',
                },
            ),
            'p_birthday': forms.SelectDateWidget(
                years=range(date.today().year - child_age, date.today().year + 1),
                attrs={
                    # 'class': 'form-control',
                    'required': True,
                    'title': '생일을 입력하세요',
                },
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
                attrs={
                    'class': 'form-control',
                    'placeholder': "전문 분야",
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '전문 분야를 입력하세요',
                }
            ),
            'c_resume': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "이력",
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '이력을 입력하세요',
                }
            ),
        }


class ChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['u_nickname'].label = '별명'
        self.fields['u_nickname'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nickname',
            # 'autocomplete': 'off',
            'required': True,
            'title': '별명을 입력하세요'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e-mail',
            # 'autocomplete': 'off',
            'required': True,
            'title': 'e-mail을 입력하세요',
        })

    class Meta:
        model = User
        fields = ('u_nickname', 'u_contact', 'email')

        labels = {
            'u_contact': '전화번호',
        }

        widgets = {
            'u_contact': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "000-0000-0000",
                    # 'autocomplete': 'off',
                    'required': True,
                    'title': '전화번호를 입력하세요',
                }
            ),
        }
