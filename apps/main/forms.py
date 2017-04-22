from django import forms
from .models import *


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ('file_data','file_type', 'owner', 'authorized_users', 'parent_folder', 'is_in_trash', 'stars')