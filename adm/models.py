from django.db import models
from modelos.models import Usuario

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(Usuario)

    website = models.URLField(blank=True)
    telefono = models.CharField(max_length=50)