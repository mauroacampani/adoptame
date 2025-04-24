from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .form import UserRegisterForm, FormReset
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

# Create your views here.
def index(request):
    return render(request, 'portal/index.html')


class RegistroUsuarioView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'registration/registroUsuario.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print(form)
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

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            messages.error(self.request, "El correo no está registrado")
            return redirect('/users/resetPasswordEmail')

        # Generar token y UID
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Crear enlace con token
        reset_link = f"http://127.0.0.1:8000/recuperarPassword/{uid}/{token}/"

        # Enviar correo con el enlace
        email_message = EmailMessage(
            subject="Recuperación de contraseña",
            body=f'Para restablecer la contraseña, haga clic en el siguiente enlace:\n{reset_link}',
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        email_message.send(fail_silently=False)

        messages.success(
            self.request, "Se ha enviado un correo con instrucciones para restablecer la contraseña.")
        return redirect('/')
    


def reset_password_confirm(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Users.objects.get(pk=uid)
    except (Users.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
            elif len(password1) < 8:
                messages.error(
                    request, "La contraseña debe tener al menos 8 caracteres.")
            else:
                user.set_password(password1)
                user.save()
                # Mantiene la sesión iniciada si aplica
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Contraseña actualizada correctamente. Inicia sesión con tu nueva contraseña.")
                return redirect('/')  # Redirige a la página de inicio o login

        return render(request, 'registration/reset_password_form.html', {'user': user})

    else:
        messages.error(request, "El enlace no es válido o ha expirado.")
        return redirect('/')