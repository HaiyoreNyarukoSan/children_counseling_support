from django import forms

from board.models import Article, Communication, C_Comment, CounselorReview
from users.models import Counselor


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        writer = kwargs.pop('a_writer') if 'a_writer' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['a_patient'].label = '상담 받을 자녀분'
        if writer:
            self.fields['a_patient'].queryset = writer.patient_set
        self.fields['a_title'].label = '제목'
        self.fields['a_content'].label = '내용'
        self.fields['a_tree_image'].label = "나무 이미지"
        self.fields['a_man_image'].label = "남자사람 이미지"
        self.fields['a_woman_image'].label = "여자사람 이미지"
        self.fields['a_house_image'].label = "집 이미지"
        self.fields['a_patient'].empty_label = None
        self.fields['a_patient'].label_from_instance = lambda patient: patient.p_name
        self.fields['a_patient'].widget.attrs.update({
            'class': 'form-control',
            # 'autocomplete': 'off',
            'required': True,
            'title': '상담 받을 자녀분을 골라주세요',
        })
        self.fields['a_title'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'name': 'name',
            'id': 'name',
            'placeholder': '제목을 입력하세요',
            'required': 'required'})
        self.fields['a_content'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '4',
            'name': 'message',
            'id': 'message',
            'placeholder': '내용을 입력하세요',
            'required': 'required'
        })
        self.fields['a_tree_image'].widget = forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'style': 'font-family: Jua; margin-bottom: 10px;',
            'required': False,
        })
        self.fields['a_man_image'].widget = forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'style': 'font-family: Jua; margin-bottom: 10px;',
        })
        self.fields['a_woman_image'].widget = forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'style': 'font-family: Jua; margin-bottom: 10px;',
        })

        self.fields['a_house_image'].widget = forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'style': 'font-family: Jua; margin-bottom: 10px;',
        })

    class Meta:
        model = Article
        fields = ['a_patient', 'a_title', 'a_content', 'a_tree_image', 'a_man_image', 'a_woman_image', 'a_house_image']

        labels = {
            'a_title': '제목',
            'a_content': '내용'
        }


class CommunicationForm(forms.ModelForm):
    com_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    com_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Communication
        fields = ['com_title', 'com_content']

        labels = {
            'com_title': '글 제목',
            'com_content': '글 내용'
        }

        widgets = {
            'com_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'name',
                    'id': 'name',
                    'placeholder': '제목을 입력하세요',
                    'required': 'required'
                }
            ),

            'com_content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                    'name': 'message',
                    'id': 'message',
                    'placeholder': '내용을 입력하세요',
                    'required': 'required'
                }
            )
        }


class C_CommentForm(forms.ModelForm):
    cc_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = C_Comment
        fields = ['cc_content']

        labels = {

            'cc_content': '글 내용'
        }

    widgets = {

        'cc_content': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4',
                'name': 'review',
                'id': 'review',
                'placeholder': '내용을 입력하세요',
                'required': 'required'
            }
        )

    }


class CounselorReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['r_patient'].label = '상담 받을 자녀분'
        self.fields['r_content'].label = '글 내용'
        self.fields['r_patient'].empty_label = None
        self.fields['r_patient'].label_from_instance = lambda patient: patient.p_name
        self.fields['r_patient'].widget.attrs.update({
            'class': 'form-control',
            # 'autocomplete': 'off',
            'required': True,
            'title': '상담 받을 자녀분을 골라주세요',
        })
        self.fields['r_content'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4',
                'name': 'review',
                'id': 'review',
                'placeholder': '내용을 입력하세요',
                'required': 'required'
            }
        )

    class Meta:
        model = CounselorReview
        fields = ['r_patient', 'r_content']


class EditArticleForm(forms.ModelForm):
    a_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    a_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = ['a_title', 'a_content']

        labels = {
            'a_title': '제목',
            'a_content': '내용'
        }
        widgets = {
            'a_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'name',
                    'id': 'name',
                    'placeholder': '제목을 입력하세요',
                    'required': 'required'
                }
            ),

            'a_content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                    'name': 'message',
                    'id': 'message',
                    'placeholder': '내용을 입력하세요',
                    'required': 'required'
                }
            )
        }


class EditCommunicationForm(forms.ModelForm):
    a_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    a_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Communication
        fields = ['com_title', 'com_content']

        labels = {
            'com_title': '제목',
            'com_content': '내용'
        }
        widgets = {
            'com_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'name': 'name',
                    'id': 'name',
                    'placeholder': '제목을 입력하세요',
                    'required': 'required'
                }
            ),

            'com_content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                    'name': 'message',
                    'id': 'message',
                    'placeholder': '내용을 입력하세요',
                    'required': 'required'
                }
            )
        }

# class CounselorForm(forms.ModelForm):
#     a_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     a_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
