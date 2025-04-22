from django.contrib.auth.models import AbstractUser
from django.db import models
from adoptame.settings import MEDIA_URL, STATIC_URL



class Users(AbstractUser):
    imagen = models.ImageField(upload_to='usuarios', null=True, blank=True)

    
    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'app/img/usuarios/iconoper.jpg')