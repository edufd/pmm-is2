from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(User)

    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    ci = models.IntegerField(unique=True)
    telefono = models.IntegerField()

    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = 'userprofile'