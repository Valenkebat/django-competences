from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Este decorador se utiliza para conectar la función con la señal post_save de User
@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        # Crea un perfil de jugador asociado al usuario recién creado
        UserProfile.objects.create(user=instance)
        

# Este decorador se utiliza para guardar el perfil de jugador cuando se guarda el usuario
@receiver(post_save, sender=User)
def save_player_profile(sender, instance, **kwargs):
    # Guarda el perfil de jugador asociado al usuario
    instance.userprofile.save()