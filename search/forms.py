from django import forms
from .models import MasterDataFile

# create model form to upload masterDatafile
class MasterDataFileForm(forms.ModelForm):
    class Meta:
        model = MasterDataFile
        fields = ('file_name', 'file')
        widgets = {
            'file_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept':'.csv'})
        }

