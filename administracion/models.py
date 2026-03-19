from django.db import models
from adoptame.settings import MEDIA_URL, STATIC_URL


# Create your models here.
class Mascotas(models.Model):

    class Estado(models.TextChoices):
        ADOPTADO = 'ADP', 'Adoptado'
        EN_ADOPCION = 'EAD', 'En Adopción'

    class Sexo(models.TextChoices):
        HEMBRA = 'HEM', 'Hembra'
        MACHO = 'MAC', 'Macho'

    class Opciones(models.TextChoices):
            SI = 'SI', 'Si'
            NO = 'NO', 'No'

    nombre = models.CharField(max_length=150)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=3, choices=Sexo.choices, default=Sexo.MACHO)
    vacuna = models.CharField(max_length=3, choices=Opciones.choices, default=Opciones.SI)
    desparacitado = models.CharField(max_length=3, choices=Opciones.choices, default=Opciones.SI)
    estado = models.CharField(max_length=3, choices=Estado.choices, default=Estado.EN_ADOPCION)
    castrado = models.CharField(max_length=3, choices=Opciones.choices, default=Opciones.SI)
    caracteristicas = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='mascotas/')
    imagen1 = models.ImageField(upload_to='mascotas/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='mascotas/', null=True, blank=True)

    def __str__(self):
        return f'{self.id}'
    
    # def get_imagen(self):
    #     if self.imagen:
    #         return '{}{}'.format(MEDIA_URL, self.imagen)
    #     return '{}{}'.format(STATIC_URL, 'app/img/usuarios/iconoper.jpg')
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)  # borrado fisico

        if self.imagen1:
            self.imagen1.storage.delete(self.imagen1.name)

        if self.imagen2:
            self.imagen2.storage.delete(self.imagen2.name)

        super().delete()


    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
 