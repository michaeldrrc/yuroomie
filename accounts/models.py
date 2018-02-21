from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField()
    gender_options = (('m', 'male'), 
                        ('f', 'female'),
                        ('o', 'other'))
    gender = models.CharField(choices=gender_options, max_length=6)
    
    def __str__(self):
        return self.user.username