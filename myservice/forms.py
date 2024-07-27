from django import forms
from .models import User

# 회원가입시 추가적인 정보 입력
from django import forms
from .models import User

class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'is_hearing_impaired', 'communication_method']
        widgets = {
            'communication_method': forms.TextInput(attrs={'placeholder': 'Enter your preferred communication method'})
        }

    def clean(self):
        cleaned_data = super().clean()
        is_hearing_impaired = cleaned_data.get('is_hearing_impaired')
        communication_method = cleaned_data.get('communication_method')

        if is_hearing_impaired and not communication_method:
            self.add_error('communication_method', 'This field is required if you are hearing impaired.')

        return cleaned_data

