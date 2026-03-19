from django.urls import path
from administracion import views


urlpatterns = [
    path('', views.index_administracion, name='index_administracion'),
    path('listadoMascotas/', views.ListMascotas.as_view(), name="listadoMascotas"),
    path('registroMascotas/', views.RegistroMascotasView.as_view(), name="registroMascotas"),
    path('editarMascota/<id>', views.EditarMascota.as_view(), name="editarMascota"),
]