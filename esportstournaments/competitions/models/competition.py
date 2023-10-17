from django.db import models
from django.contrib.auth.models import User
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES

class Competition(models.Model):
    name = models.CharField(default="Competition Name", max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    competition_type = models.CharField(max_length=20, choices=(
        ('liga', 'Liga'),
        ('eliminacion_directa', 'Eliminación Directa'),
        ('doble_eliminacion', 'Doble Eliminación'),
    ))
    # if set to true the league will display on the front page, false and it will not
    active = models.BooleanField(default=False)
    info = models.TextField(default="No information provided")
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)
    bestof = models.SmallIntegerField(choices=MAPFORMAT_CHOICES, default=1)
    # team format, ex 1v1, 2v2, 3v3, 4v4
    teamformat = models.SmallIntegerField(choices=TEAMFORMAT_CHOICES, default=1)
    # by default its a best of 1. Not sure if we need this here. Finals might be best of 3, etc in
    # the future possibly. TBD. For now this will work though.
    image = models.ImageField(upload_to='tournament_images', blank=True)
     # when does registration open, and when does it close? specified when created in staff panel
    open_register = models.DateTimeField()
    # dont allow people to join once registration is closed
    close_register = models.DateTimeField()
    allow_register = models.BooleanField(default=False)

    def __str__(self):
        return self.name