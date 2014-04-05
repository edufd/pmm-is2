from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    telefono = models.CharField(max_length=50)