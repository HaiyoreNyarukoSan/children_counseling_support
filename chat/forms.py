from django import forms

from chat.models import chat_room


class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        reviewer = kwargs.pop('reviewer') if 'reviewer' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['r_patient'].label = '상담 받을 자녀분'
        if reviewer:
            self.fields['r_patient'].queryset = reviewer.patient_set

        self.fields['r_patient'].empty_label = None
        self.fields['r_patient'].label_from_instance = lambda patient: patient.p_name
        self.fields['r_patient'].widget.attrs.update({
            'class': 'form-control',
            # 'autocomplete': 'off',
            'required': True,
            'title': '상담 받을 자녀분을 골라주세요',
        })

    class Meta:
        model = chat_room
        fields = ['r_patient']
