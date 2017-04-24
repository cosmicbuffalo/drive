from django import forms
from .models import *


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = [
            'file_data',            
        ]


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = [
            "name",
        ]
