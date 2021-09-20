from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    phone = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    