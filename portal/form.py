#FORM REGISTRO DE USUARIO
from django import forms
from portal.models import Users
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

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
    

#FORM PARA CAMBIAR EL PASSWORD DEL USUARIO
class cambiarPasswordForm(PasswordChangeForm):
    model = Users
    fields = '__all__'



class cambiarPasswordeMailForm(forms.Form):

    password1 = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una contraseña',
        'class': 'form-control form-control-sm',
        'autocomplete': 'off',
        'size': '25'
    }))

    password2 = forms.CharField(label='Confirmación de contraseña nueva', widget=forms.PasswordInput(attrs={
        'placeholder': 'Repetir contraseña',
        'class': 'form-control form-control-sm',
        'autocomplete': 'off'
    }))

    def clean_password1(self):
        data = self.cleaned_data['password1']
       
        if len(data) < 8:
            raise forms.ValidationError('Las contraseña')
        return data
    
    # def clean(self):
    #     cleaned = super().clean()
    #     password1 = cleaned['password1']
    #     password2 = cleaned['password2']

    #     if password1 != password2:
    #         raise forms.ValidationError('Las contraseña deben ser iguales')
    #     return cleaned
    

    
    