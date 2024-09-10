from django import forms
from .models import CompanyFile
from django.utils.translation import gettext_lazy as _


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CompanyFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return file
