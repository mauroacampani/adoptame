from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('registroUsuario/', views.RegistroUsuarioView.as_view(), name="registroUsuario"),
    path('resetPasswordEmail', views.ResetPasswordEmailView.as_view(), name='resetPasswordEmail'),
    path('recuperarPassword/<uidb64>/<token>/', views.reset_password_confirm, name='recuperarPassword'),
    path('cambiarPassword/', views.CambiarPasswordView.as_view(), name='cambiarPassword'),
]