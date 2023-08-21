from django import forms

from board.models import Article


class ArticleForm(forms.ModelForm):
    a_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    a_content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    a_tree_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn-outline-primary btn-sm',
        'style': 'font-family: Jua; margin-bottom: 10px;',
    }), required=False, label="나무 이미지")

    a_man_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn-outline-primary btn-sm',
        'style': 'font-family: Jua; margin-bottom: 10px;',
    }), required=False, label="남자사람 이미지")

    a_woman_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn-outline-primary btn-sm',
        'style': 'font-family: Jua; margin-bottom: 10px;',
    }), required=False, label="여자사람 이미지")

    a_house_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'btn btn-outline-primary btn-sm',
        'style': 'font-family: Jua; margin-bottom: 10px;',
    }), required=False, label="집 이미지")

    class Meta:
        model = Article
        fields = ['a_title', 'a_content', 'a_tree_image', 'a_man_image', 'a_woman_image', 'a_house_image']

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
        ),
        'a_tree_image': forms.ImageField(widget=forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'type': 'file',
            'id': 'inputImage1',
            'name': 'image1',
            'accept': 'image/*',
            'style': 'font-family: Jua; margin-bottom: 10px;'
        }), required=False, label=''),

        'a_man_image': forms.ImageField(widget=forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'type': 'file',
            'id': 'inputImage2',
            'name': 'image2',
            'accept': 'image/*',
            'style': 'font-family: Jua; margin-bottom: 10px;'
        }), required=False, label=''),

        'a_woman_image': forms.ImageField(widget=forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'type': 'file',
            'id': 'inputImage3',
            'name': 'image3',
            'accept': 'image/*',
            'style': 'font-family: Jua; margin-bottom: 10px;'
        }), required=False, label=''),

        'a_house_image': forms.ImageField(widget=forms.ClearableFileInput(attrs={
            'class': 'btn btn-outline-primary btn-sm',
            'type': 'file',
            'id': 'inputImage4',
            'name': 'image4',
            'accept': 'image/*',
            'style': 'font-family: Jua; margin-bottom: 10px;'
        }), required=False, label='')

    }
