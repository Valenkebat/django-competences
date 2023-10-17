from django.db import models
from .competition import Competition

class DoubleEliminationCompetition(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE, parent_link=True)
    # Agregar campos específicos para Double Elimination