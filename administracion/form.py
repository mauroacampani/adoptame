from django import forms
from .models import Mascotas

class formMascotas(forms.ModelForm):
 
    class Meta:
        model = Mascotas
        
        fields = '__all__'