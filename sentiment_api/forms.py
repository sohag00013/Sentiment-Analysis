from django import forms
from .models import LargeTextArea

class LargeTextAreaForm(forms.ModelForm):
    class Meta:
        model = LargeTextArea
        fields = ['content']