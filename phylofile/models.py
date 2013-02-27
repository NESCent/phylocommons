from django.db import models
from django.contrib.auth.models import User
from phylofile.signals import create_profile


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_text = models.TextField(max_length=5000)
    
    
models.signals.post_save.connect(create_profile, sender=User)
