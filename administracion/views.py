from django.shortcuts import render, redirect
from administracion.models import Mascotas
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from administracion.form import formMascotas
from django.http import Http404

# Create your views here.
def index_administracion(request):    
    variable = 'test variable'
    return render(request, 'administracion/index_administracion.html', {'variable': variable})


class ListMascotas(ListView):
    model = Mascotas
    template_name = 'administracion/mascotas/listadoMascotas.html'  # La plantilla que se va a renderizar
    context_object_name = 'mascotas'  # Nombre de la variable que se pasará al contexto

    #permission_required = 'mascotas.view_mascotas'

    def get_queryset(self):
        # Definimos el queryset que se va a mostrar en la lista, con el ordenamiento por 'estado'
        return Mascotas.objects.all().order_by('estado')
    

class RegistroMascotasView(CreateView):
    model = Mascotas
    form_class = formMascotas
    template_name = 'administracion/mascotas/registroMascotas.html'

    #permission_required = 'mascotas.add_mascotas'

    def form_valid(self, form):

        if not form.is_valid():
            messages.error(self.request, "El formulario contiene errores.")
            return self.render_to_response(self.get_context_data(form=form))

        post = form.save(commit=False)

        if 'imagen' in form.cleaned_data and form.cleaned_data['imagen']:
            image = form.cleaned_data['imagen']
            resized_image = redimencionar_imagen(image)
            post.imagen = resized_image

        if 'imagen1' in form.cleaned_data and form.cleaned_data['imagen1']:
            image = form.cleaned_data['imagen1']
            resized_image = redimencionar_imagen(image)
            post.imagen1 = resized_image

        if 'imagen2' in form.cleaned_data and form.cleaned_data['imagen2']:
            image = form.cleaned_data['imagen2']
            resized_image = redimencionar_imagen(image)
            post.imagen2 = resized_image


        try:
            post.save()
        except Exception as e:
     
            messages.error(self.request, f"Hubo un error al guardar la mascota: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

   
        messages.add_message(self.request, messages.SUCCESS, "La mascota fue registrada correctamente.")

        return redirect('listadoMascotas') 

    def form_invalid(self, form):
        # Si el formulario es inválido, devolvemos el contexto con el formulario y los errores
        messages.error(self.request, "El formulario contiene errores. Por favor, revisa los campos.")
        return self.render_to_response(self.get_context_data(form=form))

import os

class EditarMascota(UpdateView):
    model = Mascotas
    form_class = formMascotas
    template_name = 'administracion/mascotas/editarMascotas.html'
    context_object_name = 'mascota'

    #permission_required = 'mascotas.update_mascotas'

    
    def form_valid(self, form):
        
        mascota = self.get_object()

        vieja_imagen = mascota.imagen
        vieja_imagen1 = mascota.imagen1
        vieja_imagen2 = mascota.imagen2

        post = form.save(commit=False)

        # Asignamos nuevas imágenes si se subieron
        if 'imagen' in form.cleaned_data.get('imagen'):
            post.imagen = form.cleaned_data['imagen']

        if form.cleaned_data.get('imagen1'):
            post.imagen1 = form.cleaned_data['imagen1']

        if form.cleaned_data.get('imagen2'):
            post.imagen2 = form.cleaned_data['imagen2']

        post.save()  # Guardamos con las nuevas imágenes

        # Ahora sí, eliminamos las imágenes anteriores si se subieron nuevas
        if form.cleaned_data.get('imagen') and vieja_imagen and vieja_imagen != post.imagen:
            if os.path.isfile(vieja_imagen.path):
                os.remove(vieja_imagen.path)

        if form.cleaned_data.get('imagen1') and vieja_imagen1 and vieja_imagen1 != post.imagen1:
            if os.path.isfile(vieja_imagen1.path):
                os.remove(vieja_imagen1.path)

        if form.cleaned_data.get('imagen2') and vieja_imagen2 and vieja_imagen2 != post.imagen2:
            if os.path.isfile(vieja_imagen2.path):
                os.remove(vieja_imagen2.path)

        messages.add_message(self.request, messages.SUCCESS, "Se editó la mascota correctamente")
        
        return redirect('listadoMascotas')

   
    def get_object(self, queryset=None):
        
        try:
            return Mascotas.objects.get(pk=self.kwargs['id'])
        except Mascotas.DoesNotExist:
            raise Http404("La mascota no existe")

 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'files': self.request.FILES})  # importante para imágenes
    #     return kwargs
    

from PIL import Image
import io
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def redimencionar_imagen(image):
    if image is None:
        return None  # Si no hay imagen, devolvemos None (o puedes lanzar un error si lo prefieres)

    # Si la imagen está presente, procesamos la imagen
    img = Image.open(image)
    
    # Redimensionamos la imagen (por ejemplo, 800x800)
    img = img.resize((800, 800), Image.LANCZOS)

    # Guardamos la imagen redimensionada en un archivo temporal
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)

    # Creamos un archivo InMemoryUploadedFile para poder guardarlo en el modelo
    image_file = InMemoryUploadedFile(
        img_io, None, image.name, 'image/jpeg', img_io.tell(), None
    )

    return image_file