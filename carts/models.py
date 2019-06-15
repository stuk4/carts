from datetime import datetime
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Perfil(models.Model):
    tipos = (('Propietario','Propietario'),
            ('Normal','Normal'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50,blank=True,null=True)
    telefono = models.PositiveIntegerField(blank=True,null=True)
    tipo = models.CharField(max_length=20,choices=tipos,default='Normal',null=True)


@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_perfil(sender, instance, **kwargs):
    instance.perfil.save()

class Carrito(models.Model):
    estados = (('Aceptado','Aceptado'),
                ('Rechazado','Rechazado'),
                ('Pendiente','Pendiente'))
    solicitante = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40,default='Desconocido',null=True)
    nombre_dueño = models.CharField(max_length=40,default='Desconocido',null=True)
    direccion = models.CharField(max_length=60)
    descripcion = models.TextField(null=True)
    estado = models.CharField(max_length=20,choices=estados,default='Pendiente')
    def __str__(self):
        return self.nombre
    


class Productos(models.Model):
    carritos = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d', blank=True)
    precio = models.PositiveIntegerField()
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre