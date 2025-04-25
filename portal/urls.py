from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    # path('mensaje/', views.mensaje, name='mensaje'),

    path('registroUsuario/', views.RegistroUsuarioView.as_view(), name="registroUsuario"),
    path('resetPasswordEmail', views.ResetPasswordEmailView.as_view(), name='resetPasswordEmail'),

    path('cambiarPassword/', views.CambiarPasswordView.as_view(), name='cambiarPassword'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('password-reset-confirm/<uidb64>/<token>/', views.validate_token_and_redirect, name='validate_token'),
    path('set-password/', views.set_new_password, name='set_new_password'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]