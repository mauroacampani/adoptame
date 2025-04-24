#FORM REGISTRO DE USUARIO
from django import forms
from portal.models import Users
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = Users
        fields = ['username', 'password1', 'password2', 'email']
    
    def clean_email(self):
        email1 = self.cleaned_data['email']
    
        email_usuario = Users.objects.filter(email=email1)
        
        if email_usuario:
            raise forms.ValidationError("El email existe")
        return email1
    
    def clean_username(self):
        username = self.cleaned_data['username']
    
        user_usuario = Users.objects.filter(username=username)
        
        if user_usuario:
            raise forms.ValidationError("El usuario ya existe")
        return username
    

class FormReset(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su Email',
        'class': 'form-control form-control-sm',
        'autocomplete': 'off',
    }))
    class Meta:
        model = Users
        fields = ['email']
    #email = forms.EmailField(required=True)

    def clean_email(self):
        email1 = self.cleaned_data['email']
        
        email_usuario = Users.objects.filter(email=email1)
        
        if not email_usuario:
            raise forms.ValidationError("El email no existe")
        return email1