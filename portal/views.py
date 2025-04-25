from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .form import UserRegisterForm, FormReset, cambiarPasswordForm
from .models import Users
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

# Create your views here.
def index(request):
    return render(request, 'portal/index.html')


class RegistroUsuarioView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'registration/registroUsuario.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        
        usuario = form.save()

        group = Group.objects.get(name='usuario')
        group.user_set.add(usuario)

        messages.add_message(self.request, messages.SUCCESS,
                             "Usuario creado correctamente")

        return super().form_valid(form)



class ResetPasswordEmailView(FormView):
    template_name = 'registration/formResetPassword.html'
    form_class = FormReset

    def form_valid(self, form):
        email = form.cleaned_data['email']

        user = Users.objects.get(email=email)
        
        # Generar token y UID
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)


         # Usar reverse + build_absolute_uri en vez de hardcodear la URL
        reset_link = self.request.build_absolute_uri(
            reverse('validate_token', kwargs={'uidb64': uid, 'token': token})
        )
       
        # Enviar correo con el enlace
        email_message = EmailMessage(
            subject="Recuperación de contraseña",
            body=f'Para restablecer la contraseña, haga clic en el siguiente enlace:\n{reset_link}',
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
       
        # Enviar el correo
        email_message.send()

        messages.success(
            self.request, "Se ha enviado un correo con instrucciones para restablecer la contraseña.")
        return redirect('resetPasswordEmail')
    

    
#CAMBIAR PASSWORD DE LOS USUARIO, CADA USUARIO PODRA CAMBIAR SU PASSWORD
class CambiarPasswordView(FormView):
    template_name = 'registration/cambiarPassword.html'
    form_class = cambiarPasswordForm
    success_url = reverse_lazy('cambiarPassword')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Aquí se pasa el usuario al formulario
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Para mantener la sesión activa
        messages.add_message(self.request, messages.SUCCESS, "La contraseña se ha cambiado correctamente")
        return super().form_valid(form)
    

# def mensaje(request):
#     return render(request, 'portal/mensaje.html')


User = get_user_model()


def validate_token_and_redirect(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['reset_user_id'] = user.id
        return redirect('set_new_password')
    else:
        return render(request, 'registration/token_invalid.html')
    

def set_new_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('resetPasswordEmail')

    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_user_id']
            return redirect('password_reset_complete')
    else:
        form = SetPasswordForm(user)

    return render(request, 'registration/set_new_password.html', {'form': form})