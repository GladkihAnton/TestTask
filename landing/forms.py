from django import forms
from landing.models import FileImage


class FileImageForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=True)

    class Meta:
        model = FileImage
        fields = ('file', 'height', 'width', )
